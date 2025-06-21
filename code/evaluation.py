import evaluate
from tqdm import tqdm

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, Wav2Vec2ProcessorWithLM

from datasets import load_dataset, load_from_disk

import torch


import os
import argparse
import logging
import pandas as pd 
import re

def setup_logging(log_file=None):
    """
    Set up logging to print messages to the console and optionally save to a log file.
    """
    log_handlers = [logging.StreamHandler()]
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        log_handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=log_handlers,
    )
    logging.info("Logging setup complete.")
    
def main():
    parser = argparse.ArgumentParser(description="Code to evaluate predictions.")
    parser.add_argument("--all", type=bool, required=False, default=True, help="Run evaluation on all three test sets (FLEURS, ALFAA, BABEL)")
    parser.add_argument("--dataset", type=str, required=False, help="Name of test datset (FLEURS, ALFAA, or BABEL)")
    parser.add_argument("--log_file", type=str, help="Optional log file for saving logs.")    
    parser.add_argument("--model", type=str, required=True, help="Path to ASR model")
    parser.add_argument("--hf_token", type=str, help="Huggingface token.")
    
    parser.add_argument("--output", type=str,  help="Path to save predictions.")
    
    
    args = parser.parse_args()
    
    setup_logging(args.log_file)
    logging.info("Preparing test datasets...")

    
    
    if args.all:
        fleurs= load_dataset("google/xtreme_s", "fleurs.am_et")['test']
        alfaa= load_from_disk("alffaa_data.hf")['test']
        
        test_data={'fleurs':fleurs, 'alfaa':alfaa}
    else:
        if args.dataset.lower()=='fleurs':
            fleurs= load_dataset("google/xtreme_s", "fleurs.am_et")['test']
            test_data={'fleurs':fleurs}
        elif args.dataset.lower()=='alfaa':
            alfaa= load_from_disk("alffaa_data.hf")['test']
            test_data={'alfaa':alfaa}
    
    
    logging.info("Loading model...")
    model = Wav2Vec2ForCTC.from_pretrained(args.model, token=args.hf_token).to("cuda")
    processor = Wav2Vec2Processor.from_pretrained(args.model, token=args.hf_token)
    
    if re.search("mms", args.model):
        logging.info("Setting up Amharic config for MMS")
        processor.tokenizer.set_target_lang('amh')
        model.load_adapter('amh')
        
    xtreme_s_metric = evaluate.load('xtreme_s', 'fleurs-asr')
    with torch.no_grad():
        for name, testset in test_data.items():
            predictions=[]
            references=[]
            logging.info("Generating predictions for " +name +" with " + args.model)
            for test_sample in tqdm(testset):
                    try:
                        input_dict = processor(test_sample['audio']['array'], return_tensors="pt", padding=True, sampling_rate=16_000)
                        logits = model(input_dict.input_values.to("cuda")).logits
                        pred_ids=torch.argmax(logits, dim=-1)[0]
                        predictions.append(processor.decode(pred_ids))
                        references.append(test_sample['transcription'])
                    except:
                        print("Could not generate prediction for ", test_sample['transcription'])
                    
            pred_df=pd.DataFrame()
            pred_df['references']=references
            pred_df['predictions']=predictions
            
            logging.info("Saving predictions...")
            pred_df.to_csv(os.path.join(args.output, "_".join([name, args.model, "predictions.csv"])), "w")
            
            logging.info("Calculating Score...")
            
            print(xtreme_s_metric.compute(predictions=predictions, references=references))


if __name__=="__main__":
    main()
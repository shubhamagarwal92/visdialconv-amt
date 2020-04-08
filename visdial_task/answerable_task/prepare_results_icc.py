import json
import argparse
import pandas as pd
from collections import defaultdict, Counter
import random
from typing import List
import csv


class ResultsAnalyzer:
    def __init__(self, results_jsonpath: str,
                 save_data_dir: str):
        self.results_jsonpath = results_jsonpath
        self.save_data_dir = save_data_dir
        self.options_normalizer = {
            "hist_info": 1,
            "correctly": 2,
            "common_sense": 3,
            "guess": 4,
            "cant_tell": 5,
            "not_relevant": 6
        }
        self.index2word = {
            index: word for word, index in self.options_normalizer.items()
        }


        self.options_normalizer_with_mapping = {
            "hist_info": 1,
            "correctly": 2,
            "common_sense": 3,
            "guess": 3,
            "cant_tell": 4,
            "not_relevant": 4
        }
        self.index2word_mapping = {
            index: word for word, index in self.options_normalizer_with_mapping.items()
        }


    @staticmethod
    def json_load(file_path):
        with open(file_path, "r") as fb:
            data = json.load(fb)
        return data

    @staticmethod
    def json_dump(file_path: str, data_dump):
        with open(file_path, 'w') as outfile:
            json.dump(data_dump, outfile)

    @staticmethod
    def write_list_to_file(filepath, write_list):
        with open(filepath, 'w') as file_handler:
            for item in write_list:
                file_handler.write("{}\n".format(item))
        # outfile.write("\n".join(itemlist))
        return

    @staticmethod
    def read_amt_results(file_path):
        amt_results = []
        with open(file_path, "r") as fb:
            for line in fb:
                amt_results.append(json.loads(line))
        return amt_results

    @staticmethod
    def most_common(lst):
        return max(set(lst), key=lst.count)

    @staticmethod
    def _save_file_path(save_data_dir: str,
                        mapping: bool = False,
                        batch: str = '2_5') -> str:
        file_path = f"{save_data_dir}/visdial_crowdsource_mapping_{str(mapping)}_batch_{batch}_icc.csv"
        print("Saving in: ", file_path)
        return file_path

    def get_analysis(self, mapping=False, batch: str = '1'):
        amt_results = self.read_amt_results(self.results_jsonpath)
        print("Total AMT hits: ", len(amt_results))
        # print(amt_results[0].keys())
        self.get_stats_dic(amt_results, mapping=mapping, batch=batch)

    def get_stats_dic(self, amt_results: List,
                      mapping: bool,
                      batch: str = '1'):

        worker_dic = defaultdict(int)
        curated_response_dic = defaultdict(list)

        for hit in amt_results:
            hit_results = hit['output']  # actual output per each hit
            for indx in range(len(hit_results)):
                image_id = hit_results[indx]['image_id']
                if mapping:
                    option = self.options_normalizer_with_mapping[hit_results[indx]['option']]  # integer now
                else:
                    option = self.options_normalizer[hit_results[indx]['option']]  # integer now
                curated_response_dic[image_id].append(option)
            worker_dic[hit['worker_id']] += 1

        print("Total unique images which got all responses: ", len(curated_response_dic))

        non_agreement_images = []
        write_file_path = self._save_file_path(self.save_data_dir, mapping=mapping, batch=batch)
        stats_dic = defaultdict(int)

        # CSV Writing in the format required by R script
        outfile = open(write_file_path, 'w')
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(['img', 'judge', 'response'])

        considered_images = 0
        hist_info_images = []

        for img, response in curated_response_dic.items():
            # writer = csv.DictWriter(outfile, ['img', 'judge' 'response'], delimiter=',')
            # writer.writeheader()
            for indx in range(len(response)):
                writer.writerow([img, indx, response[indx]])

            counter = Counter(response)
            # counter gives list[(value,count)]
            most_common_val = counter.most_common(1)[0][0]
            # If more than two voted for same element -
            # so counter would be less than 3
            # print(counter)
            if len(counter) == 1 or len(counter) == 2:
                stats_dic[most_common_val] += 1
                considered_images += 1
                # Considered hist info images
                # So value == 1
                if most_common_val == 1:
                    hist_info_images.append(img)
            else:
                non_agreement_images.append(img)

        outfile.close()

        print("Total images with non agreement: ", len(non_agreement_images))
        print("% discarded: ", len(non_agreement_images)/len(curated_response_dic)*100)
        print("Total images considered for stats:", considered_images)
        print("Non agreement images: ", non_agreement_images)
        print("Images requiring hist info: ", hist_info_images)

        hist_info_images_path = f"{self.save_data_dir}/visdial_img_ids_hist_info_batch_{batch}.txt"
        self.write_list_to_file(filepath=hist_info_images_path, write_list=hist_info_images)

        stats = pd.DataFrame(stats_dic.items(), columns=['option', 'count'])
        stats['percent'] = stats['count']*100/stats['count'].sum()

        if mapping:
            stats["option"].replace(self.index2word_mapping, inplace=True)
        else:
            stats["option"].replace(self.index2word, inplace=True)
        stats = stats.sort_values(by=['count'], ascending=False)
        print(stats)

        # Extra information about unique workers
        unique_workers = Counter(worker_dic)
        print("Unique workers: ", unique_workers.most_common())
        print("Total Unique workers: ", len(unique_workers.most_common()))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--results_jsonpath", default="",
        help="Path to result json"
    )

    parser.add_argument(
        "-s", "--save_data_dir", default="",
        help="Path to save analysis."
    )
    args = parser.parse_args()
    return args


def main(args):
    results_analyzer = ResultsAnalyzer(args.results_jsonpath,
                                       args.save_data_dir)
    results_analyzer.get_analysis(mapping=False, batch="1_5")
    results_analyzer.get_analysis(mapping=True, batch="1_5")


if __name__ == '__main__':
    args = parse_args()
    main(args)

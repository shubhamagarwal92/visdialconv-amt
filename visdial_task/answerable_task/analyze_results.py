import json
import argparse
import pandas as pd
from collections import defaultdict, Counter
import random


class ResultsAnalyzer:
    def __init__(self, results_jsonpath: str,
                 save_analysis_path: str):
        self.results_jsonpath = results_jsonpath
        self.save_analysis_path = save_analysis_path

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
    def read_amt_results(file_path):
        amt_results = []
        with open(file_path, "r") as fb:
            for line in fb:
                amt_results.append(json.loads(line))
        return amt_results

    def get_analysis(self):
        amt_results = self.read_amt_results(self.results_jsonpath)
        print("Total AMT hits: ", len(amt_results))
        print(amt_results[0].keys())
        worker_dic = defaultdict(int)
        count_hit_disapproved = 0
        curated_response_dic = defaultdict(list)
        non_curated_response_dic = defaultdict(list)
        # test_images =
        for hit in amt_results:
            worker_id = hit['worker_id']
            assignment_id = hit['assignment_id']
            hit_id = hit['hit_id']
            hit_results = hit['output']  # actual output per each hit
            response_default_correctly = hit_results[0]['option']  # First response should be "correctly"
            response_default_hist_info = hit_results[1]['option']  # Second response should be "hist_info"
            if response_default_correctly == "correctly" and response_default_hist_info == "hist_info":
                for indx in range(2, len(hit_results)):
                    image_id = hit_results[indx]['image_id']
                    option = hit_results[indx]['option']
                    curated_response_dic[image_id].append(option)
                worker_dic[hit['worker_id']] += 1
            else:
                print(f"Ignoring hit for Worker: {worker_id} hit: {hit_id} assignment: {assignment_id}")

                img_id_default_correctly = hit_results[0]['image_id']
                img_id_default_hist_info = hit_results[1]['image_id']

                print(f"Option chosen: Correctly: {response_default_correctly} "
                      f"for id: {img_id_default_correctly} and Hist info: {response_default_hist_info} "
                      f"for {img_id_default_hist_info}")
                count_hit_disapproved += 1

        print("Total unique images which got one response: ", len(curated_response_dic))
        print(curated_response_dic)
        print("Total hits that can be disapproved: ", count_hit_disapproved)

        stats_dic = defaultdict(int)

        curated_responses_per_image = defaultdict(int)
        for img, response in curated_response_dic.items():
            curated_responses_per_image[len(response)] += 1

            if len(response) ==3:
                print("Image with all the three answers",img)

            if len(response) > 1:
                if "hist_info" in response:
                    stats_dic["hist_info"] += 1
                else:
                    stats_dic[random.choice(response)] += 1
            else:
                stats_dic[response[0]] += 1

        print("Number of curataed responses per image: ", curated_responses_per_image)
        stats = pd.DataFrame(stats_dic.items(), columns=['option', 'count'])
        stats['percent'] = stats['count']*100/stats['count'].sum()
        stats = stats.sort_values(by=['count'], ascending=False)
        print(stats)

        # Extra information about unique workers
        # unique_workers = Counter(worker_dic)
        # print("Unique workers: ", unique_workers.most_common())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--results_jsonpath", default="",
        help="Path to result json"
    )
    parser.add_argument(
        "-s", "--save_analysis_path", default="",
        help="Path to save analysis."
    )
    args = parser.parse_args()
    return args


def main(args):
    results_analyzer = ResultsAnalyzer(args.results_jsonpath,
                                       args.save_analysis_path)
    results_analyzer.get_analysis()


if __name__ == '__main__':
    args = parse_args()
    main(args)

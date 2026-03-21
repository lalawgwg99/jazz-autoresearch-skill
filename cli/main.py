import argparse, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.result_tracker import ResultTracker
from core.experiment import ExperimentEngine
from hypothesis.generator import LLMHypothesisGenerator
from core.env_sentinel import EnvSentinel

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('run')
    sub.add_parser('status')
    sub.add_parser('plot')
    sub.add_parser('insights')
    sub.add_parser('diagnose')
    args = parser.parse_args()
    if args.command == 'diagnose':
        print(EnvSentinel().get_report())
    elif args.command == 'run':
        sentinel = EnvSentinel()
        print('Diagnosing environment...')
        print(sentinel.get_report())
        gen = LLMHypothesisGenerator()
        hypo = gen.generate_next_hypothesis()
        print('Running: ' + str(hypo.get("hypothesis_description")))
        ExperimentEngine().run_experiment(hypo)
    elif args.command == 'status':
        print('Best BPB: ' + str(ResultTracker().get_best_score()))
        print('History:\n' + ResultTracker().get_history_summary())
    elif args.command == 'plot':
        from cli.plot import plot_progress
        plot_progress()
    elif args.command == 'insights':
        from core.insight_generator import InsightGenerator
        InsightGenerator().update_insights()

if __name__ == '__	main__': main()

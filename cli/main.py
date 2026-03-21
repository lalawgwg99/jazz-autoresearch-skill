import argparse, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.result_tracker import ResultTracker
from core.experiment import ExperimentEngine
from hypothesis.generator import LLMHypothesisGenerator

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('run')
    sub.add_parser('status')
    sub.add_parser('plot')
    sub.add_parser('insights')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        gen = LLMHypothesisGenerator()
        eng = ExperimentEngine()
        hypo = gen.generate_next_hypothesis()
        print('Running: ' + str(hypo.get('hypothesis_description')))
        eng.run_experiment(hypo)
    elif args.command == 'status':
        t = ResultTracker()
        print('Best BPB: ' + str(t.get_best_score()))
        print('History:
' + t.get_history_summary())
    elif args.command == 'plot':
        from cli.plot import plot_progress
        plot_progress()
    elif args.command == 'insights':
        from core.insight_generator import InsightGenerator
        InsightGenerator().update_insights()

if __name__ == '__main__':
    main()
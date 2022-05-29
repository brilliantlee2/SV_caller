import argparse
def set_parser():
	parser = argparse.ArgumentParser()

	parser.add_argument('-errlen', type=int, default=300, help='Acceptable range of structural variation positions.')
	parser.add_argument('-vcf1', type=str, required=True, help='The prefix of input first vcf format file.')
	parser.add_argument('-vcf2', type=str, required=True, help='The prefix of input second vcf format file.')


	return parser.parse_known_args()[0]
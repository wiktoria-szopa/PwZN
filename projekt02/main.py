from Ising import Ising
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('n', type=int, help='rozmiar boków siatki')
parser.add_argument('J', type=float, help='wartość całki wymiany')
parser.add_argument('beta', type=float, help='parametr związany z temperaturą')
parser.add_argument('B', type=float, help='wartość pola B')
# makrokroków, czyli ile razy losujemy tyle spinow ile jest lacznie w siatce, czyli
# majac np n=2, to 2 kroki to byloby losowanie 8 razybo 4 to calkowita ilosc spinow, a 2*4=8
parser.add_argument('step_number', type=int, help='liczba kroków symulacji')
parser.add_argument('rho', type=float, help='początkowa gęstość spinów w górę', default=0.5)
parser.add_argument('--pictures', '-p', help='nazwa folderu z generowanymi obrazkami')
parser.add_argument('--animate', '-a', help='nazwa pliku z animacją')
parser.add_argument('--magnetisation', '-m', help='nazwa pliku z magnetyzacją')
args = parser.parse_args()

tmp = Ising(args.n, args.J, args.beta, args.B, args.step_number, args.rho, args.pictures, args.animate, args.magnetisation)
tmp.simulate()

# python projekt02/main.py 20 1 1 1 4 0.5 -p projekt02/pics -a projekt02/animate.gif -m projekt02/magnetisation.txt
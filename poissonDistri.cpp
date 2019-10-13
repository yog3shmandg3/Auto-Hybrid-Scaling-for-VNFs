#include <iostream>
#include <random>
#include <fstream>
int main(int argc, char** argv)
{
	const int nrolls = 10000;	// number of experiments
	const int nstars = atoi(argv[1]);	// maximum number of stars to distribute
	std::default_random_engine generator;
	std::poisson_distribution<int> distribution(4.1);

	int p[10]={};

	for (int i=0; i<nrolls; ++i) {
		int number = distribution(generator);
		if (number<10) ++p[number];
	}

	std::ofstream myfile;
	myfile.open("distributedData.txt");
	std::cout << "poisson_distribution:" << std::endl;
	for (int i=0; i<10; ++i) {
		std::cout << i << ": " << std::string(p[i]*nstars/nrolls,'*') << std::endl;
		myfile << p[i]*nstars/nrolls;
		myfile << "\n";
	}
	myfile.close();
	return 0;
}

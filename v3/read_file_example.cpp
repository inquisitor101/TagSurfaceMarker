#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>


void SwapBytes
(
 void   *buffer,
 size_t  nBytes,
 int     nItems
)
 /*
	* Function, which swaps bytes.
	*/
{
	// Store half the number of bytes in kk and cast the buffer
	// to a character buffer.
	char *buf       = (char *) buffer;
	const size_t kk = nBytes/2;
	
	// Loop over the number of items in the buffer.
	for(int j=0; j<nItems; ++j)
	{
	  // Initialize ii and jj, which are used to store the
	  // indices of the bytes to be swapped.
	  size_t ii = j*nBytes;
	  size_t jj = ii + nBytes - 1;
	
	  // Swap the bytes.
	  for(size_t i=0; i<kk; ++i, ++ii, --jj)
	  {
	    const char tmp = buf[jj];
	    buf[jj] = buf[ii];
	    buf[ii] = tmp;
	  }
	}
}



int main(int argc, char **argv)
{
	if (argc != 2)
	{
		std::cout << "Must provide filename." << std::endl;
	}

	// Input file.
	std::cout << argv[1] << std::endl;

	// length of string.
	const int CGNS_STRING_SIZE = 33;

	// AS3 magic number.
	const unsigned int AS3_MAGIC_NUMBER = 3735929054; 


	// Common variables, used later for writing.
	unsigned int c_nElem;
	unsigned int c_nNode;
	unsigned int c_nMarker;
	std::vector<std::vector<double>> c_xx;
	std::vector<std::vector<double>> c_yy;
	std::vector<std::vector<std::vector<unsigned int>>> c_marker;


	/*
	 * READ BINARY FILE.
	 */

	// Open file.
	FILE *fh = std::fopen( argv[1], "rb");
	
	// Check file can be opened.
	if ( !fh )
		std::cout << "could not open file!" << std::endl;

	unsigned int        someunsignedinteger;
	int                 someinteger;
	double              somedouble;


	// Read integer.
	if( std::fread( &someunsignedinteger, sizeof(unsigned int), 1, fh ) != 1 ) exit(1);
	std::cout << "magic number: " << someunsignedinteger << std::endl;
	if (someunsignedinteger != AS3_MAGIC_NUMBER) { exit(1); }

	std::fread( &someinteger, sizeof(int), 1, fh );
	std::cout << "ndim: " << someinteger << std::endl;

	std::vector<unsigned int> someunsignedintarr(2);
	std::fread( someunsignedintarr.data(), sizeof(unsigned int), 2, fh );
	unsigned int nx = someunsignedintarr[0];
	unsigned int ny = someunsignedintarr[1];
	std::cout << "nx: " << nx << ", ny: " << ny << std::endl;

	unsigned int nNode;
	std::fread( &nNode, sizeof(unsigned int), 1, fh );
	std::cout << "nNode: " << nNode << std::endl;
	c_nNode = nNode;

	unsigned int n = nx*ny;
	c_nElem = n;
	std::vector<std::vector<double>> xx( n, std::vector<double>(nNode) );
	for(size_t i=0; i<n; i++)
		std::fread( xx[i].data(), sizeof(double), nNode, fh );
	
	c_xx = xx;
	std::cout << "x-coordinate: " << std::endl;
	for(auto& i : xx)
	{
		for(auto& j : i)
			std::cout << j << ", ";
		std::cout << std::endl;
	}	

	std::vector<std::vector<double>> yy( n, std::vector<double>(nNode) );
	for(size_t i=0; i<n; i++)
		std::fread( yy[i].data(), sizeof(double), nNode, fh );

	c_yy = yy;
	std::cout << "y-coordinate: " << std::endl;
	for(auto& i : yy)
	{
		for(auto& j : i)
			std::cout << j << ", ";
		std::cout << std::endl;
	}	

	std::vector<unsigned int> conv(4);
	std::fread( conv.data(), sizeof(unsigned int), 4, fh );
	std::cout << "convention: " << conv[0] << ", " << conv[1] << ", " << conv[2] << ", " << conv[3] << std::endl;


	unsigned int nMarker;
	std::fread( &nMarker, sizeof(unsigned int), 1, fh );
	std::cout << "nMarker: " << nMarker << std::endl;
	c_nMarker = nMarker;

	c_marker.resize(nMarker);

	for(size_t i=0; i<nMarker; i++)
	{
		char buff[CGNS_STRING_SIZE];
		std::fread( &buff[0], sizeof(char), CGNS_STRING_SIZE, fh );
		std::string name(buff);
		std::cout << "tag name: " << name << std::endl;

		unsigned int nFace;
		std::fread( &nFace, sizeof(unsigned int), 1, fh );
		std::cout << "nFace: " << nFace << std::endl;

		std::vector<std::vector<unsigned int>> marker( nFace, std::vector<unsigned int>(2) );
		for(size_t j=0; j<nFace; j++)
			std::fread( marker[j].data(), sizeof(unsigned int), 2, fh );
	
		c_marker[i] = marker;
		for(auto& k : marker)
		{
			for(auto& s : k)
				std::cout << s << ", ";
			std::cout << std::endl;
		}
	}


	// Close file
	std::fclose(fh);


	/*
	 * WRITE ASCII FILE.
	 */

	std::ofstream Output_File;

	// Open file and check if it can be opened.
	Output_File.open("output_ascii.txt", std::ios::out);
	if( !Output_File.is_open() )
	{
		std::cout << "output file could not be opened for writing." << std::endl;
		exit(1);
	}

	Output_File << "nElem: " << c_nElem << "\n";
	Output_File << "nNode: " << c_nNode << "\n";

	Output_File << "------------------------------------------\n";
	Output_File << "x-coordinates: \n";
	for(auto& i : c_xx)
	{
		for(auto& x : i)
			Output_File << x << ",";
		Output_File << "\n";
	}	

	Output_File << "------------------------------------------\n";
	Output_File << "y-coordinates: \n";
	for(auto& i : c_yy)
	{
		for(auto& y : i)
			Output_File << y << ",";
		Output_File << "\n";
	}

	Output_File << "------------------------------------------\n";
	for(size_t i=0; i<c_nMarker; i++)
	{
		Output_File << "iMarker: " << i << "\n";
		Output_File << "nFace: " << c_marker[i].size() << "\n";

		//std::cout << c_marker[i][1].size() << std::endl;
		for(auto& m : c_marker[i])
		{
			for(auto& s : m)
				Output_File << s << ",";
			Output_File << "\n";
		}
	}





	// Close the file.
	Output_File.close();

	return 0;
}













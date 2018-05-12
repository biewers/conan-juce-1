#include <cstdlib>
#include <JuceHeader.h>

int main()
{
	auto time = juce::Time::getCurrentTime();
	std::cout << "JUCE tested at " << time.toISO8601(true) << std::endl;

    return EXIT_SUCCESS;
}

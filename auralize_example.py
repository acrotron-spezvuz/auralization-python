from samples.auralize_from_env import auralize_from_env_example
from samples.auralize_from_content import auralize_from_content

if __name__ == "__main__":
    # Run Auralization with object structure build within python.
    auralize_from_env_example()

    # Run Auralization with using an input file;
    auralize_from_content("environ.txt")

import mmh3
import bitarray


class BloomFilter:

    def __init__(self, size: int, num_hashes: int):
        """
        Initializes the Bloom Filter.

        Args:
            size (int): The size of the bit array.
            num_hashes (int): The number of hash functions to use.
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray.bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item: str):
        """
        Generates multiple hash values for an item.

        Args:
            item (str): The item to hash.

        Returns:
            List[int]: A list of hash values.
        """
        hashes = []
        for i in range(self.num_hashes):
            hash_value = mmh3.hash(item, i) % self.size
            hashes.append(hash_value)
        return hashes

    def add(self, item: str):
        """
        Adds an item to the Bloom Filter.

        Args:
            item (str): The item to add.
        """
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

    def contains(self, item: str) -> bool:
        """
        Checks if an item is possibly in the Bloom Filter.

        Args:
            item (str): The item to check.

        Returns:
            bool: True if the item might be in the filter, False otherwise.
        """
        return all(self.bit_array[hash_value] for hash_value in self._hashes(item))


def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list) -> dict:
    """
    Checks if passwords are unique using a Bloom Filter.

    Args:
        bloom_filter (BloomFilter): The Bloom Filter instance.
        passwords (list): A list of passwords to check.

    Returns:
        dict: Dictionary with password statuses.
    """
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "Некоректний ввід"
        elif bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    return results


if __name__ == "__main__":
    # Initialize Bloom Filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Add existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for passwrd in existing_passwords:
        bloom.add(passwrd)

    # Check new passwords
    new_passwords_to_check = [
        "password123",
        "newpassword",
        "admin123",
        "guest",
        "",
        None,
        "  ",
    ]
    check_results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Display results
    for passwrd, status in check_results.items():
        print(f"Пароль '{passwrd}' — {status}.")

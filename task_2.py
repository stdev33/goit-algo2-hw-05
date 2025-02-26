import json
import time
from hyperloglog import HyperLogLog

log_file_path = "lms-stage-access.log"


def load_ip_addresses(file_path):
    ip_addresses = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                if "remote_addr" in log_entry:
                    ip_addresses.append(log_entry["remote_addr"])
            except json.JSONDecodeError:
                continue
    return ip_addresses


def exact_count(ip_addresses):
    """Точний підрахунок унікальних IP-адрес за допомогою множини set."""
    return len(set(ip_addresses))


def hyperloglog_count(ip_addresses):
    """Наближений підрахунок унікальних IP-адрес за допомогою HyperLogLog."""
    hll = HyperLogLog(0.01)  # Задана похибка 1%
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


if __name__ == "__main__":
    ip_list = load_ip_addresses(log_file_path)
    print(f"{len(ip_list)} IP-адрес з файлу {log_file_path} завантажено.")

    start_time = time.time()
    exact_unique_ips = exact_count(ip_list)
    exact_time = time.time() - start_time

    start_time = time.time()
    hll_unique_ips = hyperloglog_count(ip_list)
    hll_time = time.time() - start_time

    print("\nРезультати порівняння:")
    print(f"{'':25}{'Точний підрахунок':>20}{'HyperLogLog':>15}")
    print(f"{'Унікальні елементи':25}{exact_unique_ips:>20.1f}{hll_unique_ips:>15.1f}")
    print(f"{'Час виконання (сек.)':25}{exact_time:>20.2f}{hll_time:>15.6f}")

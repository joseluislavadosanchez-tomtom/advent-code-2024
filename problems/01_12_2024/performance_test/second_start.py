import random
import timeit
from collections import Counter


def result_dict(list1: list[int], list2: list[int]) -> int:
    count_list2 = Counter(list2)
    return sum(x * count_list2.get(x, 0) for x in list1)


def print_faster_result(mean_times):
    fastest_method = min(mean_times, key=mean_times.get)
    print(
        f"\nFastest Method: {fastest_method} with Mean Time: {mean_times[fastest_method]:.6f} seconds\n"
    )


def result_vec(list1: list[int], list2: list[int]) -> int:
    max_val = 100_000_000
    freq_list2 = [0] * (max_val + 1)
    for num in list2:
        freq_list2[num] += 1

    return sum(x * freq_list2[x] for x in list1)


def both_vec_result(list1: list[int], list2: list[int]) -> int:
    max_val = 100_000_000

    freq_list1 = [0] * (max_val + 1)
    for num in list1:
        freq_list1[num] += 1

    freq_list2 = [0] * (max_val + 1)
    for num in list2:
        freq_list2[num] += 1

    return sum(i * freq_list1[i] * freq_list2[i] for i, _ in enumerate(freq_list1))


def optimized_result(list1: list[int], list2: list[int]) -> int:
    count_list1 = Counter(list1)
    count_list2 = Counter(list2)
    return sum(x * count_list1[x] * count_list2[x] for x in count_list1)


def generate_random_input(size: int, max_value: int) -> tuple[list, list]:
    list1 = [random.randint(0, max_value) for _ in range(size)]
    list2 = [random.randint(0, max_value) for _ in range(size)]
    return list1, list2


if __name__ == "__main__":
    sizes = [10, 100, 1_000, 10_000, 100_000, 1_00_000, 10_000_000]
    max_value = 99_999_999
    for size in sizes:
        list1, list2 = generate_random_input(size, max_value)
        times = timeit.repeat(lambda: result_dict(list1, list2), repeat=10, number=1)
        mean_time_dict = sum(times) / len(times)
        std_time = (sum((x - mean_time_dict) ** 2 for x in times) / len(times)) ** 0.5
        print(
            f"[Dict] Size: {size}, Mean Time: {mean_time_dict:.6f} seconds, Std Dev: {std_time:.6f} seconds"
        )

        times = timeit.repeat(lambda: result_vec(list1, list2), repeat=10, number=1)
        mean_time_vec = sum(times) / len(times)
        std_time = (sum((x - mean_time_vec) ** 2 for x in times) / len(times)) ** 0.5
        print(
            f"[Vec] Size: {size}, Mean Time: {mean_time_vec:.6f} seconds, Std Dev: {std_time:.6f} seconds"
        )

        times = timeit.repeat(
            lambda: optimized_result(list1, list2), repeat=10, number=1
        )
        mean_time_opt = sum(times) / len(times)
        std_time = (sum((x - mean_time_opt) ** 2 for x in times) / len(times)) ** 0.5
        print(
            f"[Optimized] Size: {size}, Mean Time: {mean_time_opt:.6f} seconds, Std Dev: {std_time:.6f} seconds"
        )

        times = timeit.repeat(
            lambda: both_vec_result(list1, list2), repeat=10, number=1
        )
        mean_time_both = sum(times) / len(times)
        std_time = (sum((x - mean_time_both) ** 2 for x in times) / len(times)) ** 0.5
        print(
            f"[Both Vec] Size: {size}, Mean Time: {mean_time_both:.6f} seconds, Std Dev: {std_time:.6f} seconds"
        )

        # Assert all results are equal and print which one is different if not
        result_dict_val = result_dict(list1, list2)
        result_vec_val = result_vec(list1, list2)
        optimized_result_val = optimized_result(list1, list2)
        both_vec_result_val = both_vec_result(list1, list2)

        if not (
            result_dict_val
            == result_vec_val
            == optimized_result_val
            == both_vec_result_val
        ):
            if result_dict_val != result_vec_val:
                print("Mismatch: result_dict is different from result_vec")
            if result_dict_val != optimized_result_val:
                print("Mismatch: result_dict is different from optimized_result")
            if result_dict_val != both_vec_result_val:
                print("Mismatch: result_dict is different from both_vec_result")
            if result_vec_val != optimized_result_val:
                print("Mismatch: result_vec is different from optimized_result")
            if result_vec_val != both_vec_result_val:
                print("Mismatch: result_vec is different from both_vec_result")
            if optimized_result_val != both_vec_result_val:
                print("Mismatch: optimized_result is different from both_vec_result")
            raise AssertionError("Results are not equal.")
        else:
            print("All results are equal.")

        # Print which implementation is faster
        mean_times = {
            "Dict": mean_time_dict,
            "Vec": mean_time_vec,
            "Optimized": mean_time_opt,
            "Both Vec": mean_time_both,
        }
        print_faster_result(mean_times)

        print("--------------------")

    # list1 = [1] * 1000000
    # list2 = [1] * 1000000

    # times = timeit.repeat(lambda: result_dict(list1, list2), repeat=10, number=1)
    # mean_time_dict = sum(times) / len(times)
    # std_time = (sum((x - mean_time_dict) ** 2 for x in times) / len(times)) ** 0.5
    # print(
    #     f"[Dict] 10_000_000 ones, Mean Time: {mean_time_dict:.6f} seconds, Std Dev: {std_time:.6f} seconds"
    # )

    # times = timeit.repeat(lambda: result_vec(list1, list2), repeat=10, number=1)
    # mean_time_vec = sum(times) / len(times)
    # std_time = (sum((x - mean_time_vec) ** 2 for x in times) / len(times)) ** 0.5
    # print(
    #     f"[Vec] 10_000_000 ones, Mean Time: {mean_time_vec:.6f} seconds, Std Dev: {std_time:.6f} seconds"
    # )

    # times = timeit.repeat(lambda: optimized_result(list1, list2), repeat=10, number=1)
    # mean_time_opt = sum(times) / len(times)
    # std_time = (sum((x - mean_time_opt) ** 2 for x in times) / len(times)) ** 0.5
    # print(
    #     f"[Optimized] 10_000_000 ones, Mean Time: {mean_time_opt:.6f} seconds, Std Dev: {std_time:.6f} seconds"
    # )

    # times = timeit.repeat(lambda: both_vec_result(list1, list2), repeat=10, number=1)
    # mean_time_both = sum(times) / len(times)
    # std_time = (sum((x - mean_time_both) ** 2 for x in times) / len(times)) ** 0.5
    # print(
    #     f"[Both Vec] 10_000_000 ones, Mean Time: {mean_time_both:.6f} seconds, Std Dev: {std_time:.6f} seconds"
    # )

    # # Print which implementation is faster
    # mean_times = {
    #     "Dict": mean_time_dict,
    #     "Vec": mean_time_vec,
    #     "Optimized": mean_time_opt,
    #     "Both Vec": mean_time_both,
    # }
    # print_faster_result(mean_times)

    # print("--------------------")

    # # Assert all results are equal and print which one is different if not
    # result_dict_val = result_dict(list1, list2)
    # result_vec_val = result_vec(list1, list2)
    # optimized_result_val = optimized_result(list1, list2)
    # both_vec_result_val = both_vec_result(list1, list2)

    # if not (
    #     result_dict_val == result_vec_val == optimized_result_val == both_vec_result_val
    # ):
    #     if result_dict_val != result_vec_val:
    #         print("Mismatch: result_dict is different from result_vec")
    #     if result_dict_val != optimized_result_val:
    #         print("Mismatch: result_dict is different from optimized_result")
    #     if result_dict_val != both_vec_result_val:
    #         print("Mismatch: result_dict is different from both_vec_result")
    #     if result_vec_val != optimized_result_val:
    #         print("Mismatch: result_vec is different from optimized_result")
    #     if result_vec_val != both_vec_result_val:
    #         print("Mismatch: result_vec is different from both_vec_result")
    #     if optimized_result_val != both_vec_result_val:
    #         print("Mismatch: optimized_result is different from both_vec_result")
    #     raise AssertionError("Results are not equal.")
    # else:
    #     print("All results are equal.")

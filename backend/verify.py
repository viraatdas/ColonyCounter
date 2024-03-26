from count import count_colonies_within_petri_dish
import os
import re

TEST_DIRECTORY = "sample-images/test_CFU_Plate_Pics"
TOLERANCE_PERCENTAGE = 5


def extract_colony_count(filename):
    match = re.match(r'(\d+)', filename)
    if match:
        return int(match.group(1))
    return None


def is_within_tolerance(actual_count, predicted_count, tolerance_percentage):
    if actual_count == 0 and predicted_count == 0:
        return True
    elif actual_count == 0 or predicted_count == 0:
        return False
    percentage_diff = abs(actual_count - predicted_count) / actual_count * 100
    return percentage_diff <= tolerance_percentage


def evaluate_accuracy(directory, tolerance_percentage):
    total_images = 0
    total_correct = 0

    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            image_path = os.path.join(directory, filename)
            actual_count = extract_colony_count(filename)

            if actual_count is not None:
                _, predicted_count = count_colonies_within_petri_dish(
                    image_path)

                total_images += 1
                if is_within_tolerance(actual_count, predicted_count, tolerance_percentage):
                    total_correct += 1
                else:
                    print(
                        f"\033[91mIncorrect prediction for {filename}: Actual={actual_count}, Predicted={predicted_count}\033[0m")
            else:
                print(
                    f"\033[93mSkipping {filename} - Colony count not found in the filename\033[0m")

    if total_images > 0:
        accuracy = total_correct / total_images
        print(
            f"\033[92mAccuracy (within {tolerance_percentage}% tolerance): {accuracy:.2%} ({total_correct}/{total_images})\033[0m")
    else:
        print("\033[91mNo valid image files found.\033[0m")


if __name__ == '__main__':
    evaluate_accuracy(TEST_DIRECTORY, TOLERANCE_PERCENTAGE)

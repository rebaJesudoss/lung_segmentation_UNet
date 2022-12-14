{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "R4SiQlmRtCtX"
      },
      "outputs": [],
      "source": [
        "import os\n",
        "os.environ[\"TF_CPP_MIN_LOG_LEVEL\"] = \"2\"\n",
        "import numpy as np\n",
        "import cv2\n",
        "from glob import glob\n",
        "from tqdm import tqdm\n",
        "import tensorflow as tf\n",
        "from tensorflow.keras.utils import CustomObjectScope\n",
        "from metrics import dice_loss, dice_coef, iou\n",
        "from train import load_data, create_dir, tf_dataset"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "H = 512\n",
        "W = 512\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    \"\"\" Seeding \"\"\"\n",
        "    np.random.seed(42)\n",
        "    tf.random.set_seed(42)\n",
        "\n",
        "    \"\"\" Directory for storing files \"\"\"\n",
        "    create_dir(\"results\")\n",
        "\n",
        "    \"\"\" Loading model \"\"\"\n",
        "    with CustomObjectScope({'iou': iou, 'dice_coef': dice_coef, 'dice_loss': dice_loss}):\n",
        "        model = tf.keras.models.load_model(\"files/model.h5\")\n",
        "\n",
        "    \"\"\" Dataset \"\"\"\n",
        "    dataset_path = \"/media/nikhil/Seagate Backup Plus Drive/ML_DATASET/MontgomerySet\"\n",
        "    (train_x, train_y1), (valid_x, valid_y1), (test_x, test_y1) = load_data(dataset_path)\n",
        "\n",
        "    \"\"\" Predicting the mask \"\"\"\n",
        "    for x, y1, y2 in tqdm(zip(test_x, test_y1, test_y2), total=len(test_x)):\n",
        "        \"\"\" Extracing the image name. \"\"\"\n",
        "        image_name = x.split(\"/\")[-1]\n",
        "\n",
        "        \"\"\" Reading the image \"\"\"\n",
        "        ori_x = cv2.imread(x, cv2.IMREAD_COLOR)\n",
        "        ori_x = cv2.resize(ori_x, (W, H))\n",
        "        x = ori_x/255.0\n",
        "        x = x.astype(np.float32)\n",
        "        x = np.expand_dims(x, axis=0)\n",
        "\n",
        "        \"\"\" Reading the mask \"\"\"\n",
        "        ori_y1 = cv2.imread(y1, cv2.IMREAD_GRAYSCALE)\n",
        "        \n",
        "        ori_y = ori_y1 + ori_y2\n",
        "        ori_y = cv2.resize(ori_y, (W, H))\n",
        "        ori_y = np.expand_dims(ori_y, axis=-1)  ## (512, 512, 1)\n",
        "        ori_y = np.concatenate([ori_y, ori_y, ori_y], axis=-1)  ## (512, 512, 3)\n",
        "\n",
        "        \"\"\" Predicting the mask. \"\"\"\n",
        "        y_pred = model.predict(x)[0] > 0.5\n",
        "        y_pred = y_pred.astype(np.int32)\n",
        "\n",
        "        \"\"\" Saving the predicted mask along with the image and GT \"\"\"\n",
        "        save_image_path = f\"results/{image_name}\"\n",
        "        y_pred = np.concatenate([y_pred, y_pred, y_pred], axis=-1)\n",
        "\n",
        "        sep_line = np.ones((H, 10, 3)) * 255\n",
        "\n",
        "        cat_image = np.concatenate([ori_x, sep_line, ori_y, sep_line, y_pred*255], axis=1)\n",
        "        cv2.imwrite(save_image_path, cat_image)"
      ],
      "metadata": {
        "id": "RgGCSbyStG62"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}

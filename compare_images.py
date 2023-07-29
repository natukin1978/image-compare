import os
import argparse
import matplotlib.pyplot as plt
from send2trash import send2trash  # 画像をゴミ箱へ移動するためのライブラリ

class ImageComparator:
    def __init__(self, folders):
        self.folders = folders
        self.images_per_folder = self.get_images_per_folder()
        self.current_index = 0

        self.fig, self.axes = plt.subplots(1, len(self.folders), figsize=(10, 5))
        self.fig.patch.set_facecolor('dimgray')  # ウィンドウの背景色を設定
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.marked_for_deletion = [[False] * len(image_files) for image_files in self.images_per_folder]

        self.show_images()

    def get_images_per_folder(self):
        images_per_folder = []

        for folder in self.folders:
            image_files = []
            for filename in os.listdir(folder):
                if filename.endswith(".png"):
                    image_files.append(os.path.join(folder, filename))
            images_per_folder.append(image_files)

        return images_per_folder

    def show_images(self):
        for ax in self.axes:
            ax.cla()  # 現在の画像をクリア

        for j, image_files in enumerate(self.images_per_folder):
            image_path = image_files[self.current_index]
            image = plt.imread(image_path)

            if self.marked_for_deletion[j][self.current_index]:
                image = self.mark_for_deletion(image)

            self.axes[j].imshow(image)
            self.axes[j].axis('off')

        plt.show()

    def on_key_press(self, event):
        if event.key == 'right':
            self.next_image()
        elif event.key == 'left':
            self.previous_image()
        elif event.key.isdigit():  # 数字キーが押されたらマーク
            num = int(event.key)
            if 1 <= num <= len(self.folders):
                self.mark_image(num)

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.images_per_folder[0])
        self.show_images()

    def previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.images_per_folder[0])
        self.show_images()

    def mark_image(self, num):
        self.marked_for_deletion[num - 1][self.current_index] = not self.marked_for_deletion[num - 1][self.current_index]
        self.show_images()

    def mark_for_deletion(self, image):
        # 画像の外側に削除マークを付ける処理を実装
        # 例として、赤い枠で削除マークを付けることにします
        height, width, _ = image.shape
        thickness = min(height, width) // 20
        image[:thickness, :] = [255, 0, 0]  # 上側
        image[-thickness:, :] = [255, 0, 0]  # 下側
        image[:, :thickness] = [255, 0, 0]  # 左側
        image[:, -thickness:] = [255, 0, 0]  # 右側

        return image

    def delete_marked_images(self):
        for j, image_files in enumerate(self.images_per_folder):
            for i in range(len(image_files)):
                if self.marked_for_deletion[j][i]:
                    image_path = image_files[i]
                    send2trash(image_path)  # 画像をゴミ箱へ移動

def main():
    parser = argparse.ArgumentParser(description='Image Comparison Tool')
    parser.add_argument('folders', metavar='folder', type=str, nargs='+', help='Folders to compare')

    args = parser.parse_args()
    folders = args.folders

    image_comparator = ImageComparator(folders)

    # アプリケーション終了時にマークされた画像をゴミ箱へ移動
    image_comparator.delete_marked_images()

if __name__ == '__main__':
    main()

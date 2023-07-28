import os
import argparse
import matplotlib.pyplot as plt


class ImageComparator:
    def __init__(self, folders):
        self.folders = folders
        self.images_per_folder = self.get_images_per_folder()
        self.current_index = 0

        self.fig, self.axes = plt.subplots(1, len(self.folders), figsize=(10, 5))
        self.fig.patch.set_facecolor('dimgray')  # ウィンドウの背景色を設定
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

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
            self.axes[j].imshow(image)
            self.axes[j].axis('off')

        plt.show()

    def on_key_press(self, event):
        if event.key == 'right':
            self.next_image()
        elif event.key == 'left':
            self.previous_image()

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.images_per_folder[0])
        self.show_images()

    def previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.images_per_folder[0])
        self.show_images()

def main():
    parser = argparse.ArgumentParser(description='Image Comparison Tool')
    parser.add_argument('folders', metavar='folder', type=str, nargs='+', help='Folders to compare')

    args = parser.parse_args()
    folders = args.folders

    ImageComparator(folders)

if __name__ == '__main__':
    main()

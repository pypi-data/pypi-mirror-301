import nibabel as nib
import numpy as np
from rembg import remove
from PIL import Image
import io
import argparse
from tqdm import tqdm
import torch

def remove_background_nifti(input_path, output_path):
    # Load the NIFTI image
    nifti_img = nib.load(input_path)
    data = nifti_img.get_fdata()

    # Normalize the data to 0-255 range
    data_normalized = ((data - data.min()) / (data.max() - data.min()) * 255).astype(np.uint8)

    # Process each slice
    processed_slices = []
    for slice_idx in tqdm(range(data.shape[2]), desc="Processing slices"):  # Assuming the third dimension is for slices
        # Convert the slice to a PIL Image
        slice_img = Image.fromarray(data_normalized[:, :, slice_idx])
        
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        slice_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Remove background
        output = remove(img_byte_arr)

        # Convert back to numpy array
        output_array = np.array(Image.open(io.BytesIO(output)))

        # Keep only the first channel if the output is RGB
        if len(output_array.shape) == 3:
            output_array = output_array[:,:,0]

        processed_slices.append(output_array)

    # Stack processed slices
    processed_data = np.stack(processed_slices, axis=2)

    # Create a new NIFTI image and save
    new_img = nib.Nifti1Image(processed_data, nifti_img.affine, nifti_img.header)
    nib.save(new_img, output_path)

def main():
    parser = argparse.ArgumentParser(description="Remove background from NIFTI image")
    parser.add_argument('-i', '--input', required=True, help="Path to input NIFTI file")
    parser.add_argument('-o', '--output', required=True, help="Path for output NIFTI file")
    args = parser.parse_args()

    remove_background_nifti(args.input, args.output)

if __name__ == "__main__":
    main()
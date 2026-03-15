# takes in processed image, location/path, fish types, returns fish info (position, type)

import cv2
import numpy as np
import os
from pathlib import Path

def load_templates_from_folder(fish_names, images_dir="images"):
    # Load all template images for the given fish names.
    templates = {}
    
    for fish_name in fish_names:
        folder_path = Path(images_dir) / fish_name
        
        if not folder_path.exists():
            print(f"Folder '{folder_path}' does not exist")
            continue
        
        # Load all PNG files in this folder
        fish_templates = []
        for img_file in sorted(folder_path.glob("*.png")):
            img = cv2.imread(str(img_file), 0)  # Load as grayscale
            if img is not None:
                fish_templates.append(img)
                print(f"Loaded {img_file.name} for {fish_name}")
            else:
                print(f"Could not load {img_file}")
        
        if fish_templates:
            templates[fish_name] = fish_templates
        else:
            print(f"No template found for {fish_name}")
    
    return templates

def split_into_tiles(image, rows=3, cols=3):
    # Split image into grid 
    h, w = image.shape[:2]
    tile_h = h // rows
    tile_w = w // cols
    
    tiles = {}
    for row in range(rows):
        for col in range(cols):
            y1 = row * tile_h
            y2 = (row + 1) * tile_h if row < rows - 1 else h
            x1 = col * tile_w
            x2 = (col + 1) * tile_w if col < cols - 1 else w
            
            tiles[(row, col)] = image[y1:y2, x1:x2]
    
    return tiles

def resize_template_to_tile(template, tile_image, scale_fraction=0.8):
    # Resize template to fit within a tile (default 80% of tile size).
    tile_h, tile_w = tile_image.shape[:2]
    template_h, template_w = template.shape[:2]
    
    # Target size is 80% of tile dimensions
    target_w = int(tile_w * scale_fraction)
    target_h = int(tile_h * scale_fraction)
    
    # Preserve aspect ratio
    scale_w = target_w / template_w
    scale_h = target_h / template_h
    scale = min(scale_w, scale_h)
    
    new_w = int(template_w * scale)
    new_h = int(template_h * scale)
    
    return cv2.resize(template, (new_w, new_h), interpolation=cv2.INTER_AREA)

def match_template_in_tile(tile_image, template, min_scale=0.75, max_scale=1.25, 
                          num_scales=15, threshold=0.65):
    """
    Match a single template in a single tile at multiple scales.
    """
    matches = []
    (tH, tW) = template.shape[:2]
    
    for scale in np.linspace(min_scale, max_scale, num_scales):
        new_h = int(tH * scale)
        new_w = int(tW * scale)
        
        if new_h > tile_image.shape[0] or new_w > tile_image.shape[1]:
            continue
        if new_h < 10 or new_w < 10:
            continue
        
        resized_template = cv2.resize(template, (new_w, new_h), interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(tile_image, resized_template, cv2.TM_CCOEFF_NORMED)
        
        # Find best match in this tile
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            matches.append({
                'x': max_loc[0],
                'y': max_loc[1],
                'width': new_w,
                'height': new_h,
                'confidence': float(max_val),
                'scale': scale
            })
    
    # Return best match if any found
    if matches:
        return max(matches, key=lambda m: m['confidence'])
    return None

def is_tile_empty(tile_image, darkness_threshold=200, dark_pixel_ratio=0.05):
    """
    Check if a tile is empty (mostly white background with no significant shadows).
    
    Args:
        tile_image: The tile to check
        darkness_threshold: Pixels darker than this are considered "dark" (0-255)
        dark_pixel_ratio: Minimum ratio of dark pixels to consider tile non-empty
    
    Returns:
        True if tile is empty, False if it contains something
    """
    # Count how many pixels are significantly darker than white
    dark_pixels = np.sum(tile_image < darkness_threshold)
    total_pixels = tile_image.size
    
    # If more than X% of pixels are dark, tile is not empty
    return (dark_pixels / total_pixels) < dark_pixel_ratio

def detect_fish(processed_image, fish_names, images_dir="images", 
                threshold=0.65, tile_scale=0.8):
    """
    Detect fish in a 3x3 tiled image.
    Note: Always includes "mine" detection and "shadow" detection automatically.
    
    Args:
        processed_image: The processed grayscale image (output from imgfilter)
        fish_names: List of fish types to detect, e.g., ["sardine", "tuna"]
        images_dir: Path to the images folder
        threshold: Minimum confidence for detection (0-1)
        tile_scale: How much of the tile the template should fill (0-1)
    
    Returns:
        List of tuples: [(tile_position, fish_name, confidence), ...]
        fish_name can be a specific fish, "mine", "shadow" (unidentified), or None (empty)
    """
    # Always include mine detection
    if "mine" not in fish_names:
        fish_names = list(fish_names) + ["mine"]
    
    # Load all templates
    print("Loading templates...")
    templates = load_templates_from_folder(fish_names, images_dir)
    
    if not templates:
        print("Error: No templates loaded!")
        return []
    
    # Split image into 3x3 tiles
    print("\nSplitting image into 3x3 tiles...")
    tiles = split_into_tiles(processed_image, rows=3, cols=3)
    
    # Detect in each tile
    detections = []
    
    for tile_pos, tile_img in tiles.items():
        row, col = tile_pos
        print(f"\nSearching tile ({row}, {col})...")
        
        # First check if tile is empty
        if is_tile_empty(tile_img):
            print(f"  Tile is empty")
            continue  # Don't add to detections, skip this tile
        
        best_match = None
        best_fish = None
        
        # Try each fish type
        for fish_name, fish_templates in templates.items():
            # Try each template variant for this fish
            for template in fish_templates:
                # Resize template to fit tile
                template_resized = resize_template_to_tile(template, tile_img, tile_scale)
                
                # Match in this tile
                match = match_template_in_tile(tile_img, template_resized, threshold=threshold)
                
                # Keep track of best match for this tile
                if match and (best_match is None or match['confidence'] > best_match['confidence']):
                    best_match = match
                    best_fish = fish_name
        
        # Determine what to report for this tile
        if best_match:
            # Found a matching template
            detections.append((tile_num, best_fish, best_match['confidence']))
            print(f"  Found {best_fish} with confidence {best_match['confidence']:.3f}")
        else:
            # Tile is not empty but no template matched - it's a shadow/unknown
            detections.append((tile_num, "shadow", 0.0))
            print(f"  Found unidentified object (shadow)")
    
    return detections
    
def visualize_detections(processed_image, detections, output_path="detections.png"):
    # Draw boxes around detected fish on the image.
    # Convert to color for visualization
    output = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR) if len(processed_image.shape) == 2 else processed_image.copy()
    
    h, w = processed_image.shape[:2]
    tile_h = h // 3
    tile_w = w // 3
    
    # Single color for all detections
    color = (255, 0, 0)
    
    # Draw tile grid
    for i in range(1, 3):
        cv2.line(output, (0, i * tile_h), (w, i * tile_h), (128, 128, 128), 1)
        cv2.line(output, (i * tile_w, 0), (i * tile_w, h), (128, 128, 128), 1)
    
    # Draw detections
    for tile_num, fish_name, confidence in detections:
        row, col = divmod(tile_num - 1, 3)
        
        # Calculate tile boundaries
        x1 = col * tile_w
        y1 = row * tile_h
        x2 = (col + 1) * tile_w if col < 2 else w
        y2 = (row + 1) * tile_h if row < 2 else h
        
        # Draw rectangle around tile
        cv2.rectangle(output, (x1, y1), (x2, y2), color, 3)
        
        # Draw label
        label = f"{fish_name}" #{confidence:.2f}"
        cv2.putText(output, label, (x1 + 5, y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    cv2.imwrite(output_path, output) 
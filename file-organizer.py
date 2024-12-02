import os
import shutil
from pathlib import Path
import logging 
from datetime import datetime

def setup_logging():
    """Set up logging to track file operations"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(f'file_organizer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler()
        ]
    )

def get_file_category(extension): 
    """Determine the category of a file based on its extensions"""
    categories = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.heic', '.tiff', '.webp'],
        'videos': ['.mov', '.mp4', '.avi', '.wmv', '.flv', '.mkv', '.webm'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xlsx', '.xls', '.ppt', '.pptx'],
        'audio': ['.mp3', '.wav', '.flac', '.m4a', '.aac'],
        'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    }

    extension = extension.lower()
    for category, exts in categories.items():
        if extension in exts:
            return category 
    return 'others'      #my default misc folder :) 

def organize_files(desktop_path):
    """Organize files from desktop into categorized folders"""
    desktop = Path(desktop_path)

    #skip if path does not exist
    if not desktop.exists():
        logging.error(f"Desktop path {desktop_path} does not exist")
        return 
    
    #create organized folder 
    organized_folder = desktop / "Organized_Files"
    organized_folder.mkdir(exist_ok=True)

    #Track statistics
    stats = {'total':0, 'moved':0, 'skipped': 0 }

    for file_path in desktop.glob('*'):  # Get all files/folders
        if file_path.is_file():
            stats['total'] += 1

        #skip the script and the log fiel
        if file_path.name.startswith('file_organizer'):
            stats['skipped'] += 1
            continue

        #get category and create category folder 
        category = get_file_category(file_path.suffix)
        category_folder = organized_folder / category 
        category_folder.mkdir(exist_ok=True)

        #move file to an appropriate folder 
        try: 
            new_path = category_folder / file_path.name 
            #handle duplicate files - ex: if "file.jpg" exists, try "file_1.jpg", "file_2.jpg", etc
            if new_path.exists():
                base = new_path.stem
                extension = new_path.suffix 
                counter = 1
                while new_path.exists():
                    new_path = category_folder / f"{base}_{counter}{extension}"
                    counter += 1

            shutil.move(str(file_path), str(new_path))
            logging.info(f"Moved {file_path.name} to {category}")
            stats['moved'] += 1

        except Exception as e: 
            logging.error(f"Error moving {file_path.name}: {str(e)}")
            stats['skipped'] += 1

    return stats


if __name__ == "__main__": 
    #get desktop path
    desktop_path = str(Path.home() / "Desktop")

    # set up logging
    setup_logging()

    #run organization
    logging.info("Starting file organization...")
    stats = organize_files(desktop_path)

    #print summary
    logging.info("\nOperation Complete!")
    logging.info(f"Total files processed: {stats['total']}")
    logging.info(f"Files moved: {stats['moved']}")
    logging.info(f"Files skipped: {stats['skipped']}")

    
#!/usr/bin/env python3
"""
Photo Analyzer for HAL Photo Import System
Provides blur detection, duplicate detection, EXIF extraction, and content filtering
"""

import sys
import os
import hashlib
import json
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import cv2
import numpy as np
from datetime import datetime


class PhotoAnalyzer:
    def __init__(self):
        self.blur_threshold = 100.0  # Laplacian variance threshold
        
    def analyze_photo(self, filepath):
        """
        Comprehensive photo analysis
        Returns dict with all metadata
        """
        result = {
            'success': False,
            'error': None,
            'file_hash': None,
            'file_size': 0,
            'width': 0,
            'height': 0,
            'orientation': '',
            'mime_type': '',
            'blur_score': 0,
            'is_blurry': 'N',
            'quality_score': 0,
            'exif': {},
            'date_taken': '',
            'camera_make': '',
            'camera_model': '',
            'gps_lat': 0,
            'gps_lon': 0,
            'adult_content': 'N'
        }
        
        try:
            # File hash for duplicate detection
            result['file_hash'] = self.calculate_hash(filepath)
            result['file_size'] = os.path.getsize(filepath)
            
            # Open image
            img = Image.open(filepath)
            result['width'] = img.width
            result['height'] = img.height
            result['mime_type'] = Image.MIME.get(img.format, 'image/unknown')
            
            # Determine orientation
            if img.width > img.height:
                result['orientation'] = 'Landscape'
            elif img.height > img.width:
                result['orientation'] = 'Portrait'
            else:
                result['orientation'] = 'Square'
            
            # Extract EXIF data
            exif_data = self.extract_exif(img)
            result['exif'] = exif_data
            result['date_taken'] = exif_data.get('DateTimeOriginal', '')
            result['camera_make'] = exif_data.get('Make', '')
            result['camera_model'] = exif_data.get('Model', '')
            
            # GPS coordinates
            gps = exif_data.get('GPSInfo', {})
            if gps:
                lat, lon = self.parse_gps(gps)
                result['gps_lat'] = lat
                result['gps_lon'] = lon
            
            # Blur detection
            blur_score = self.detect_blur(filepath)
            result['blur_score'] = blur_score
            result['is_blurry'] = 'Y' if blur_score < self.blur_threshold else 'N'
            
            # Quality score (0-100)
            result['quality_score'] = self.calculate_quality_score(img, blur_score)
            
            # NSFW detection (basic - would need ML model for production)
            result['adult_content'] = self.detect_nsfw_basic(filepath)
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            
        return result
    
    def calculate_hash(self, filepath):
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def extract_exif(self, img):
        """Extract EXIF metadata from image"""
        exif_data = {}
        try:
            exif = img._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    # Handle GPS info separately
                    if tag == 'GPSInfo':
                        gps_data = {}
                        for gps_tag_id, gps_value in value.items():
                            gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            # Convert IFDRational to float
                            if hasattr(gps_value, '__iter__') and not isinstance(gps_value, (str, bytes)):
                                gps_value = [float(v) if hasattr(v, 'numerator') else v for v in gps_value]
                            elif hasattr(gps_value, 'numerator'):
                                gps_value = float(gps_value)
                            gps_data[gps_tag] = gps_value
                        exif_data[tag] = gps_data
                    else:
                        # Convert bytes to string
                        if isinstance(value, bytes):
                            value = value.decode('utf-8', errors='ignore')
                        # Convert IFDRational to float
                        elif hasattr(value, 'numerator'):
                            value = float(value)
                        # Convert tuple/list of IFDRational to floats
                        elif hasattr(value, '__iter__') and not isinstance(value, str):
                            try:
                                value = [float(v) if hasattr(v, 'numerator') else v for v in value]
                            except:
                                pass
                        exif_data[tag] = value
        except:
            pass
        return exif_data
    
    def parse_gps(self, gps_info):
        """Parse GPS coordinates from EXIF"""
        try:
            lat_ref = gps_info.get('GPSLatitudeRef', 'N')
            lat = gps_info.get('GPSLatitude', [])
            lon_ref = gps_info.get('GPSLongitudeRef', 'E')
            lon = gps_info.get('GPSLongitude', [])
            
            if lat and lon:
                # Convert to decimal degrees
                lat_decimal = self.dms_to_decimal(lat, lat_ref)
                lon_decimal = self.dms_to_decimal(lon, lon_ref)
                return lat_decimal, lon_decimal
        except:
            pass
        return 0, 0
    
    def dms_to_decimal(self, dms, ref):
        """Convert degrees/minutes/seconds to decimal"""
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal
    
    def detect_blur(self, filepath):
        """Detect blur using Laplacian variance"""
        try:
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return 0
            
            # Calculate Laplacian variance
            laplacian = cv2.Laplacian(img, cv2.CV_64F)
            variance = laplacian.var()
            return float(variance)
        except:
            return 0
    
    def calculate_quality_score(self, img, blur_score):
        """Calculate overall quality score 0-100"""
        score = 50  # Base score
        
        # Resolution bonus (up to +30)
        pixels = img.width * img.height
        if pixels >= 12000000:  # 12MP+
            score += 30
        elif pixels >= 8000000:  # 8MP+
            score += 20
        elif pixels >= 3000000:  # 3MP+
            score += 10
        
        # Blur penalty/bonus (up to +/-20)
        if blur_score > 500:
            score += 20
        elif blur_score > 200:
            score += 10
        elif blur_score < 50:
            score -= 20
        elif blur_score < 100:
            score -= 10
        
        return max(0, min(100, score))
    
    def detect_nsfw_basic(self, filepath):
        """
        Basic NSFW detection (skin tone analysis)
        For production, use a proper ML model like NudeNet
        """
        try:
            img = cv2.imread(filepath)
            if img is None:
                return 'N'
            
            # Convert to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Define skin tone range (simplified)
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # Create mask
            skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # Calculate skin percentage
            skin_pixels = np.sum(skin_mask > 0)
            total_pixels = img.shape[0] * img.shape[1]
            skin_percentage = (skin_pixels / total_pixels) * 100
            
            # Very high skin percentage might indicate NSFW
            # This is a VERY basic heuristic - use proper ML in production
            if skin_percentage > 60:
                return 'Y'
            
        except:
            pass
        
        return 'N'
    
    def compare_images(self, filepath1, filepath2):
        """
        Compare two images for similarity
        Returns similarity score 0-100
        """
        try:
            img1 = cv2.imread(filepath1, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(filepath2, cv2.IMREAD_GRAYSCALE)
            
            if img1 is None or img2 is None:
                return 0
            
            # Resize to same size for comparison
            img1 = cv2.resize(img1, (256, 256))
            img2 = cv2.resize(img2, (256, 256))
            
            # Calculate histogram correlation
            hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
            
            correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            return int(correlation * 100)
        except:
            return 0


def main():
    """Command line interface"""
    if len(sys.argv) < 3:
        print("Usage: python photo_analyzer.py <command> <filepath> [filepath2]")
        print("Commands: analyze, hash, blur, compare")
        sys.exit(1)
    
    command = sys.argv[1]
    filepath = sys.argv[2]
    
    analyzer = PhotoAnalyzer()
    
    if command == 'analyze':
        result = analyzer.analyze_photo(filepath)
        print(json.dumps(result, indent=2, default=str))
    
    elif command == 'hash':
        hash_val = analyzer.calculate_hash(filepath)
        print(hash_val)
    
    elif command == 'blur':
        score = analyzer.detect_blur(filepath)
        print(f"Blur score: {score}")
        print(f"Is blurry: {'Yes' if score < 100 else 'No'}")
    
    elif command == 'compare':
        if len(sys.argv) < 4:
            print("Compare requires two filepaths")
            sys.exit(1)
        filepath2 = sys.argv[3]
        similarity = analyzer.compare_images(filepath, filepath2)
        print(f"Similarity: {similarity}%")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()

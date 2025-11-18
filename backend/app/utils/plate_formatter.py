import re

class PlateFormatter:
    """Turkish license plate formatter and validator"""
    
    @staticmethod
    def format_plate(plate_text: str) -> str:
        """
        Format Turkish plate: 34ABC123 or 34AB1234
        """
        if not plate_text:
            return ""
        
        # Remove spaces and special characters
        plate_text = re.sub(r'[^A-Z0-9]', '', plate_text.upper())
        
        # Turkish plate patterns: 2 digits + 2-3 letters + 2-4 digits
        patterns = [
            r'^(\d{2})([A-Z]{2,3})(\d{2,4})$',  # 34ABC123
            r'^(\d{2})([A-Z]{1})(\d{4,5})$',     # 34A1234
        ]
        
        for pattern in patterns:
            match = re.match(pattern, plate_text)
            if match:
                return ''.join(match.groups())
        
        return plate_text
    
    @staticmethod
    def validate_plate(plate_text: str) -> bool:
        """
        Validate Turkish license plate format
        """
        if not plate_text:
            return False
        
        plate_text = re.sub(r'[^A-Z0-9]', '', plate_text.upper())
        
        patterns = [
            r'^\d{2}[A-Z]{2,3}\d{2,4}$',
            r'^\d{2}[A-Z]{1}\d{4,5}$',
        ]
        
        return any(re.match(pattern, plate_text) for pattern in patterns)
    
    @staticmethod
    def beautify_plate(plate_text: str) -> str:
        """
        Add spaces for display: 34 ABC 123
        """
        formatted = PlateFormatter.format_plate(plate_text)
        if len(formatted) >= 7:
            return f"{formatted[:2]} {formatted[2:-4]} {formatted[-4:]}"
        return formatted
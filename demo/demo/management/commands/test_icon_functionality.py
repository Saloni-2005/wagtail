from django.core.management.base import BaseCommand
from wagtail.contrib.navigation.models import Menu, MenuItem
from wagtail.images.models import Image
from django.core.files.images import ImageFile
from PIL import Image as PILImage
import io
import os


class Command(BaseCommand):
    help = 'Test icon functionality and create sample icons for menu items'

    def handle(self, *args, **options):
        self.stdout.write('=== Testing Icon Functionality ===')
        
        # Test 1: Check if images exist in the system
        self.test_existing_images()
        
        # Test 2: Create a test icon if none exist
        self.create_test_icon()
        
        # Test 3: Assign icons to menu items
        self.assign_icons_to_menu_items()
        
        self.stdout.write(self.style.SUCCESS('Icon functionality test completed'))

    def test_existing_images(self):
        """Check what images are available in the system"""
        self.stdout.write('\n--- Test 1: Checking Existing Images ---')
        
        try:
            images = Image.objects.all()
            self.stdout.write(f'Found {images.count()} images in the system:')
            
            for image in images[:5]:  # Show first 5 images
                self.stdout.write(f'  - {image.title} (ID: {image.id}) - {image.file.name}')
                
            if images.count() == 0:
                self.stdout.write(self.style.WARNING('⚠ No images found in the system'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Found {images.count()} images'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error checking images: {e}'))

    def create_test_icon(self):
        """Create a simple test icon if no images exist"""
        self.stdout.write('\n--- Test 2: Creating Test Icon ---')
        
        try:
            # Check if we already have a test icon
            test_icon = Image.objects.filter(title='Test Menu Icon').first()
            if test_icon:
                self.stdout.write(f'✓ Test icon already exists: {test_icon.title}')
                return test_icon
            
            # Create a simple colored square as a test icon
            img = PILImage.new('RGB', (64, 64), color='#007acc')
            
            # Save to BytesIO
            img_io = io.BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)
            
            # Create Django ImageFile
            image_file = ImageFile(img_io, name='test_menu_icon.png')
            
            # Create Wagtail Image object
            test_icon = Image(
                title='Test Menu Icon',
                file=image_file
            )
            test_icon.save()
            
            self.stdout.write(self.style.SUCCESS(f'✓ Created test icon: {test_icon.title} (ID: {test_icon.id})'))
            return test_icon
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating test icon: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
            return None

    def assign_icons_to_menu_items(self):
        """Assign icons to existing menu items"""
        self.stdout.write('\n--- Test 3: Assigning Icons to Menu Items ---')
        
        try:
            # Get an available image
            test_image = Image.objects.first()
            if not test_image:
                self.stdout.write(self.style.WARNING('⚠ No images available to assign as icons'))
                return
            
            # Get header menu items
            header_menu = Menu.objects.filter(slug='header').first()
            if header_menu:
                menu_items = header_menu.menu_items.all()[:2]  # Get first 2 items
                
                for item in menu_items:
                    if not item.icon:
                        item.icon = test_image
                        item.save()
                        self.stdout.write(f'✓ Assigned icon to menu item: {item.title}')
                    else:
                        self.stdout.write(f'✓ Menu item already has icon: {item.title}')
            
            # Test image rendering
            self.test_image_rendering(test_image)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error assigning icons: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

    def test_image_rendering(self, image):
        """Test if image can be rendered properly"""
        self.stdout.write('\n--- Test 4: Image Rendering ---')
        
        try:
            # Test different rendition sizes
            renditions = ['fill-20x20', 'fill-16x16', 'original']
            
            for rendition_filter in renditions:
                try:
                    if rendition_filter == 'original':
                        url = image.file.url
                        self.stdout.write(f'✓ Original image URL: {url}')
                    else:
                        rendition = image.get_rendition(rendition_filter)
                        self.stdout.write(f'✓ {rendition_filter} rendition URL: {rendition.url}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Could not create {rendition_filter} rendition: {e}'))
            
            # Check file existence
            if hasattr(image.file, 'path'):
                file_exists = os.path.exists(image.file.path)
                self.stdout.write(f'✓ Image file exists on disk: {file_exists}')
            else:
                self.stdout.write('ℹ Image file path not available (might be using cloud storage)')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error testing image rendering: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
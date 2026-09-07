#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
برنامج إدارة مشاهد الفيديو الوثائقي
Video Scene Manager - Documentary Production Tool
"""

import json
import os
from datetime import timedelta
from typing import List, Dict, Any
import csv

class VideoSceneManager:
    """فئة لإدارة مشاهد الفيديو الوثائقي"""
    
    def __init__(self, scenes_file: str = "scenes.json"):
        self.scenes_file = scenes_file
        self.scenes = []
        self.load_scenes()
    
    def load_scenes(self):
        """تحميل المشاهد من ملف JSON"""
        if os.path.exists(self.scenes_file):
            with open(self.scenes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.scenes = data.get('documentary', {}).get('scenes', [])
            print(f"✓ تم تحميل {len(self.scenes)} مشهد")
    
    def get_total_duration(self) -> str:
        """حساب المدة الكلية للفيديو"""
        total_seconds = sum(scene.get('duration_seconds', 0) for scene in self.scenes)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def get_scene_by_id(self, scene_id: int) -> Dict:
        """الحصول على مشهد معين باستخدام معرف المشهد"""
        for scene in self.scenes:
            if scene['scene_id'] == scene_id:
                return scene
        return None
    
    def list_all_scenes(self):
        """عرض قائمة بجميع المشاهد"""
        print("\n" + "="*80)
        print("📽️  قائمة المشاهد الكاملة")
        print("="*80 + "\n")
        
        for scene in self.scenes:
            scene_id = scene['scene_id']
            title = scene['title']
            duration = scene['duration_seconds']
            timing = scene['timing']
            location = scene.get('location', 'غير محدد')
            
            print(f"المشهد #{scene_id}: {title}")
            print(f"   ⏱️  المدة: {duration} ثانية ({timing})")
            print(f"   📍 المكان: {location}")
            print()
    
    def get_scene_details(self, scene_id: int):
        """عرض تفاصيل مشهد معين"""
        scene = self.get_scene_by_id(scene_id)
        
        if not scene:
            print(f"❌ المشهد #{scene_id} غير موجود")
            return
        
        print("\n" + "="*80)
        print(f"📽️  تفاصيل المشهد #{scene_id}: {scene['title']}")
        print("="*80 + "\n")
        
        print(f"⏱️  المدة: {scene['duration_seconds']} ثانية")
        print(f"🕐 التوقيت: {scene['timing']}")
        print(f"📍 المكان: {scene.get('location', 'غير محدد')}")
        
        # عرض التصوير
        if 'camera_work' in scene:
            print("\n🎥 عمل الكاميرا:")
            camera = scene['camera_work']
            print(f"   - النوع: {camera.get('type', '')}")
            print(f"   - الحركة: {camera.get('movement', '')}")
            print(f"   - التفاصيل: {camera.get('details', '')}")
        
        # عرض العناصر البصرية
        if 'visuals' in scene:
            print("\n🎨 العناصر البصرية:")
            visuals = scene['visuals']
            if 'main_elements' in visuals:
                for element in visuals['main_elements']:
                    print(f"   • {element}")
        
        # عرض التعليق الصوتي
        if 'narration' in scene:
            print("\n🎙️  التعليق الصوتي:")
            narration = scene['narration']
            print(f"   النص: {narration.get('text', '')}")
            print(f"   المدة: {narration.get('duration_seconds', 0)} ثانية")
            print(f"   النبرة: {narration.get('tone', '')}")
        
        # عرض التصميم الصوتي
        if 'sound_design' in scene:
            print("\n🔊 التصميم الصوتي:")
            sound = scene['sound_design']
            print(f"   الموسيقى: {sound.get('background_music', '')}")
            if 'ambient_sounds' in sound:
                print("   الأصوات المحيطة:")
                for sound_item in sound['ambient_sounds']:
                    print(f"      • {sound_item}")
    
    def export_to_csv(self, output_file: str = "scenes_export.csv"):
        """تصدير المشاهد إلى ملف CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['رقم المشهد', 'الاسم', 'المدة (ثانية)', 'التوقيت', 'المكان', 'نوع التصوير'])
            
            for scene in self.scenes:
                writer.writerow([
                    scene['scene_id'],
                    scene['title'],
                    scene['duration_seconds'],
                    scene['timing'],
                    scene.get('location', ''),
                    scene.get('camera_work', {}).get('type', '')
                ])
        
        print(f"✓ تم التصدير إلى {output_file}")
    
    def export_to_txt(self, output_file: str = "scenes_report.txt"):
        """تصدير تقرير نصي شامل"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("تقرير إنتاج الفيلم الوثائقي\n")
            f.write("مدير عام هيئة الموانئ البحرية - التحقيق\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"المدة الكلية: {self.get_total_duration()}\n")
            f.write(f"عدد المشاهد: {len(self.scenes)}\n\n")
            
            for scene in self.scenes:
                f.write(f"المشهد #{scene['scene_id']}: {scene['title']}\n")
                f.write(f"المدة: {scene['duration_seconds']} ثانية ({scene['timing']})\n")
                f.write(f"المكان: {scene.get('location', 'غير محدد')}\n")
                
                if 'narration' in scene:
                    f.write(f"\nالتعليق: {scene['narration'].get('text', '')}\n")
                
                f.write("-"*80 + "\n\n")
        
        print(f"✓ تم إنشاء التقرير: {output_file}")
    
    def calculate_scene_timings(self):
        """حساب التوقيتات الفعلية لكل مشهد"""
        print("\n" + "="*80)
        print("⏱️  جدول التوقيتات")
        print("="*80 + "\n")
        
        current_time = 0
        for scene in self.scenes:
            duration = scene['duration_seconds']
            start_time = current_time
            end_time = current_time + duration
            
            start_min, start_sec = divmod(start_time, 60)
            end_min, end_sec = divmod(end_time, 60)
            
            print(f"المشهد #{scene['scene_id']}: {scene['title']}")
            print(f"   {start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}")
            
            current_time = end_time
    
    def get_narration_script(self) -> List[str]:
        """استخراج السيناريو الكامل للتعليق الصوتي"""
        script = []
        for scene in self.scenes:
            if 'narration' in scene:
                narration = scene['narration']
                script.append(f"المشهد #{scene['scene_id']}: {scene['title']}")
                script.append(narration.get('text', ''))
                script.append("")
        return script
    
    def export_narration_script(self, output_file: str = "narration_script.txt"):
        """تصدير السيناريو الصوتي"""
        script = self.get_narration_script()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("سيناريو التعليق الصوتي\n")
            f.write("="*80 + "\n\n")
            f.write("\n".join(script))
        
        print(f"✓ تم حفظ السيناريو في: {output_file}")


def print_menu():
    """طباعة القائمة الرئيسية"""
    print("\n" + "="*80)
    print("🎬 برنامج إدارة مشاهد الفيديو الوثائقي")
    print("="*80)
    print("\nالخيارات:")
    print("1. عرض جميع المشاهد")
    print("2. عرض تفاصيل مشهد معين")
    print("3. حساب المدة الكلية")
    print("4. عرض جدول التوقيتات")
    print("5. تصدير إلى CSV")
    print("6. تصدير تقرير نصي")
    print("7. تصدير السيناريو الصوتي")
    print("8. خروج")
    print("\n" + "="*80)


def main():
    """الدالة الرئيسية"""
    manager = VideoSceneManager()
    
    while True:
        print_menu()
        choice = input("\nاختر رقم الخيار: ").strip()
        
        if choice == "1":
            manager.list_all_scenes()
        
        elif choice == "2":
            try:
                scene_id = int(input("أدخل رقم المشهد: "))
                manager.get_scene_details(scene_id)
            except ValueError:
                print("❌ الرجاء إدخال رقم صحيح")
        
        elif choice == "3":
            total = manager.get_total_duration()
            print(f"\n⏱️  المدة الكلية للفيديو: {total}")
        
        elif choice == "4":
            manager.calculate_scene_timings()
        
        elif choice == "5":
            manager.export_to_csv()
        
        elif choice == "6":
            manager.export_to_txt()
        
        elif choice == "7":
            manager.export_narration_script()
        
        elif choice == "8":
            print("\n👋 شكراً لاستخدام البرنامج!")
            break
        
        else:
            print("❌ خيار غير صحيح. الرجاء المحاولة مرة أخرى.")


if __name__ == "__main__":
    main()

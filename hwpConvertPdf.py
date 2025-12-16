import os

import win32com.client as win32

os.chdir('C:\\Python\\convert\\example\\')

for i in os.listdir():
    os.rename(i, i.replace(' - 복사본 ', ''))
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")

import win32gui
hwnd = win32gui.FindWindow(None, "빈 문서 1 - 한글")
hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckModule")
BASE_DIR = 'C:\\Python\\convert\\example\\'

print(os.listdir())

for i in os.listdir():
    if not i.lower().endswith('.hwp'): # HWP 파일만 처리
        continue
        
    hwp.Open(os.path.join(BASE_DIR, i))
    pdf_path = os.path.join(BASE_DIR, i.replace('.hwp', '.pdf'))
    
    # 1. FileSaveAsPdf 액션 기본 설정 불러오기
    hwp.HAction.GetDefault("FileSaveAsPdf", hwp.HParameterSet.HFileOpenSave.HSet)
    
    # 2. 파일 경로 설정
    hwp.HParameterSet.HFileOpenSave.filename = pdf_path
    
    # 3. 포맷 설정 (문자열 "PDF")
    hwp.HParameterSet.HFileOpenSave.Format = "PDF"
    
    # 4. PDF/A 속성 설정 (PDF/A-1b를 위한 값 256)
    # 한글 프로그램의 버전 및 설정에 따라 이 값이 달라질 수 있습니다.
    hwp.HParameterSet.HFileOpenSave.Attributes = 256 # PDF/A-1b
    
    # 5. 액션 실행
    hwp.HAction.Execute("FileSaveAsPdf", hwp.HParameterSet.HFileOpenSave.HSet)
    
    print(f"✓ {i} -> PDF/A 변환 완료")

hwp.Quit() # 작업 완료 후 한글 프로그램 종료



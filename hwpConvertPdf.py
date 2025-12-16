import os
import win32com.client as win32

hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.SetMessageBoxMode(0) 
# 파일 경로 모듈 등록 (오픈 시 경고 방지)
hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckModule")
BASE_DIR = 'c:\\Python\\convert\\example\\'

for i in os.listdir():
    if not i.lower().endswith('.hwp'):
        continue
        
    hwp_path = os.path.join(BASE_DIR, i)
    pdf_path = os.path.join(BASE_DIR, i.replace('.hwp', '.pdf'))
    
    # HWP 파일 열기
    hwp.Open(hwp_path, "HWP", "forceopen:true")
    
    # PDF/A-1b로 저장 (Attributes = 256)
    hwp.HAction.GetDefault("FileSaveAsPdf", hwp.HParameterSet.HFileOpenSave.HSet)
    hwp.HParameterSet.HFileOpenSave.filename = pdf_path
    hwp.HParameterSet.HFileOpenSave.Format = "PDF"
    hwp.HParameterSet.HFileOpenSave.Attributes = 256 # PDF/A-1b
    hwp.HAction.Execute("FileSaveAsPdf", hwp.HParameterSet.HFileOpenSave.HSet)
    
    print(f"✓ {i} -> PDF/A 변환 완료")
    
    # 3. 문서 닫기 (다음 파일을 열기 전에 저장 여부 묻지 않고 닫기)
    hwp.Close(0) 

# 모든 작업 완료 후 프로그램 종료
hwp.Quit()
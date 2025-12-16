import os
import win32com.client as win32
import extract_text as et

try:
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.SetMessageBoxMode(0)
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckModule")

    BASE_DIR = 'c:\\Python\\convert\\example\\hwp\\'
    pdf_files = []

    for i in os.listdir(BASE_DIR):
        print(f"\n🔄 {i} 변환 시작...")
        if not i.lower().endswith('.hwp') or i.lower().endswith('.hwpx'):
            print(f"❗ {i} 는 한글 파일이 아니므로 건너뜁니다.")
            continue
            
        hwp_path = os.path.join(BASE_DIR, i)
        pdf_path = os.path.join(BASE_DIR, i.replace('.hwp', '.pdf'))
        
        # HWP 파일 열기
        hwp.Open(hwp_path, "HWP", "forceopen:true;nowarning:true;")
        
        # PDF/A-1b로 저장 (Attributes = 256)
        hwp.HAction.GetDefault("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)
        hwp.HParameterSet.HFileOpenSave.filename = pdf_path
        hwp.HParameterSet.HFileOpenSave.Format = "PDF"
        hwp.HParameterSet.HFileOpenSave.Attributes = 256 # PDF/A-1b
        hwp.HAction.Execute("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)
        
        print(f"✓ {i} -> PDF/A 변환 완료")
        pdf_files.append(pdf_path)
        
        # 3. 문서 닫기 (다음 파일을 열기 전에 저장 여부 묻지 않고 닫기)
        hwp.HAction.Run("FileClose")

    # 모든 작업 완료 후 프로그램 종료
    hwp.Quit()
    
except Exception as e:
    print(f"❌ 변환 중 오류 발생: {i} - {str(e)}")

print("\n" + "=" * 50)
print("PDF 텍스트 추출 시작 (Phase 2/2)")
print("=" * 50)

if not pdf_files:
    print("변환된 PDF 파일이 없어 추출 작업을 건너뜁니다.")
else:
    for pdf_path in pdf_files:
        file_name = os.path.basename(pdf_path)
        print(f"\n[추출 파일]: {file_name}")
        
        try:
            # 전체 경로(pdf_path)를 추출 클래스에 전달
            extractor = et.PDFTextExtractor(pdf_path)
            extractor.extract_text()
            
        except Exception as e:
            print(f"❌ 텍스트 추출 중 오류 발생: {file_name} - {str(e)}")
//Write a program using Selenium WebDriver to select the number of students who have
scored more than 60 in any one subject (or all subjects). Perform data extraction and
analysis.
import org.junit.Test;
import jxl.*;
import jxl.read.*;
import jxl.write.*;
import java.io.*;
public class practical_6 {
		@Test
		public void testImportexport1() throws Exception {
			FileInputStream fi = new FileInputStream("D:\\myBook.xls");
			Workbook w = Workbook.getWorkbook(fi);
			Sheet s = w.getSheet(0);
			String a[][] = new String[s.getRows()][s.getColumns()];
			FileOutputStream fo = new FileOutputStream("D:\\myBookres.xls");
			WritableWorkbook wwb = Workbook.createWorkbook(fo);
			WritableSheet ws = wwb.createSheet("result",0);
			int c = 0;
			for(int i = 0; i < s.getRows();i++) {
			for(int j = 0; j < s.getColumns();j++)
			{
					if(i >= 1)
					{	String b = new String();
						b = s.getCell(3,i).getContents();
						int x = Integer.parseInt(
								b);
						if(x < 60)
						{
							c++;
							break;
						}
					}
					a[i][j]=s.getCell(j,i).getContents();
					Label l2 = new Label(j, i-c, a[i][j]);
					ws.addCell(l2);
			}}				
			wwb.write();
			wwb.close();
			
		}
		public static void main(String[] args) {
			
		}
		
	}


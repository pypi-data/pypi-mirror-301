//Write a program using Selenium WebDriver to update 10 student records in an Excel
file. Perform data manipulation and verification.
import org.junit.BeforeClass;
import org.junit.Test;
import jxl.*;
import jxl.read.biff.*;
import jxl.write.*;
import java.io.*;

public class practical_5 {
	@BeforeClass
	public static void f1()
	{}
	@Test
	public void testImportexport1() throws Exception {
		FileInputStream fi = new FileInputStream("D:\\myBook.xls");
		Workbook w = Workbook.getWorkbook(fi);
		Sheet s = w.getSheet(0);
		String a[][] = new String[s.getRows()][s.getColumns()];
		FileOutputStream fo = new FileOutputStream("D:\\myBookResult.xls");
		WritableWorkbook wwb = Workbook.createWorkbook(fo);
		WritableSheet ws = wwb.createSheet("result1",0);
		for(int i = 0; i < s.getRows();i++)
		for(int j = 0; j < s.getColumns();j++)
		{
			a[i][j] = s.getCell(j,i).getContents();
			Label l2 = new Label(j,i,a[i][j]);
			ws.addCell(l2);
			Label l1 = new Label(6,0,"Result");
			ws.addCell(l1);
		}
		for(int i = 1; i < s.getRows();i++)
			for(int j = 2; j < s.getColumns();j++)
			{
				a[i][j] = s.getCell(j,i).getContents();
				int x = Integer.parseInt(a[i][j]);
				if(x > 35)
				{
					Label l1 = new Label(6,i,"pass");
					ws.addCell(l1);
				}
				else
				{
					Label l2 = new Label(6,i,"fail");
					ws.addCell(l2);
					break;
				}
				
				
			}
		wwb.write();
		wwb.close();
		
	}
	public static void main(String[] args) {
		
	}
	
}

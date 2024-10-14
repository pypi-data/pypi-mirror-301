//Install Selenium Server (Selenium RC) and demonstrate its usage by executing a script
in Java or PHP to automate browser actions.

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
public class Prac_3 {
    static String driverPath = "D:/Selenium/geckodriver/geckodriver.exe";
    public static WebDriver driver;
    public static void main(String[] args) {     
        System.out.println("Selenium Demo.....");
        System.setProperty("webdriver.gecko.driver", driverPath);
        WebDriver driver = new FirefoxDriver();
        driver.get("https://www.facebook.com/");
        driver.manage().window().maximize();
    }
}
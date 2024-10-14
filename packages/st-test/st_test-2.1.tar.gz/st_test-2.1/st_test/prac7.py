//Write a program using Selenium WebDriver to provide the total number of objects
present or available on a web page. Perform object identification and counting.

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.WebElement;

public class practical_7 {
	static String driverPath = "D:/Selenium/geckodriver/geckodriver.exe";
    public static WebDriver driver;

    public static void main(String[] args) {
        System.setProperty("webdriver.gecko.driver", driverPath);
        FirefoxOptions capabilities = new FirefoxOptions();
        capabilities.setCapability("marionette", true);
        driver = new FirefoxDriver(capabilities);
        driver.get("https://www.facebook.com/");
        
        java.util.List<WebElement> links = driver.findElements(By.tagName("a"));
        System.out.println("Total links are " + links.size());
        
        for (int i = 0; i < links.size(); i++) {
            System.out.println("Link " + i + " Link name: " + links.get(i).getText());
        }

 
    }
}

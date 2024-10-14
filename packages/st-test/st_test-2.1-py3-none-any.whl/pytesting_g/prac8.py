// Write a program using Selenium WebDriver to get the number of items in a list or
combo box on a web page. Perform element identification and counting.

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

import java.util.List;

public class prac8 {
	static String driverPath = "D:/Selenium/geckodriver/geckodriver.exe";

    public static void main(String[] args) {
        System.setProperty("webdriver.gecko.driver", driverPath);
        WebDriver driver = new FirefoxDriver();  
        driver.get("https://www.google.co.in/");  

        // Count the number of links on the page
        List<WebElement> links = driver.findElements(By.tagName("a"));
        int linkCount = links.size();
        System.out.println("TOTAL NO OF LINKS = " + linkCount);

        // Count the number of buttons on the page
        List<WebElement> buttons = driver.findElements(By.tagName("button"));
        int buttonCount = buttons.size();
        System.out.println("TOTAL NO OF BUTTONS = " + buttonCount);

        // Count the number of input fields on the page
        List<WebElement> inputFields = driver.findElements(By.tagName("input"));
        int inputFieldCount = inputFields.size();
        System.out.println("TOTAL NO OF INPUT FIELDS = " + inputFieldCount);

       
    }
}

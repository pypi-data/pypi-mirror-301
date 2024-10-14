//Write a program using Selenium WebDriver to automate the login process on a specific
web page. Verify successful login with appropriate assertions.

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class practical_4 {
    static String driverPath = "D:\\Selenium\\geckodriver\\geckodriver.exe";

    public static void main(String[] args) {
        // Set system property for GeckoDriver
        System.setProperty("webdriver.gecko.driver", driverPath);
        // Initialize Firefox WebDriver
        WebDriver driver = new FirefoxDriver();

        // Open the URL
        driver.get("https://demo.openmrs.org/openmrs/");

        // Enter username
        driver.findElement(By.id("username")).sendKeys("Admin");

        // Enter password
        driver.findElement(By.id("password")).sendKeys("Admin123");

        // Select "Inpatient Ward" from the location dropdown
        driver.findElement(By.id("Inpatient Ward")).click();

        // Click on the login button
        driver.findElement(By.id("loginButton")).click();

        // Maximize the browser window
        driver.manage().window().maximize();
    }
}
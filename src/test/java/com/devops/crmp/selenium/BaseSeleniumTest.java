package com.devops.crmp.selenium;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

import java.io.File;
import java.time.Duration;

/**
 * Abstract Base Selenium Test establishing embedded Spring Boot Web Environment
 * and headless Chromium/Edge WebDriver lifecycle for CI and local verification.
 * 
 * Student: Rushikesh Gawade (23102A0052)
 * Project: Customer Review Moderation Portal (CRMP) - Task 9
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ExtendWith(SeleniumScreenshotExtension.class)
public abstract class BaseSeleniumTest {

    @LocalServerPort
    protected int port;

    protected WebDriver driver;

    @BeforeEach
    public void setUpWebDriver() {
        String chromePath = System.getenv("LOCALAPPDATA") + "\\Google\\Chrome\\Application\\chrome.exe";
        File chromeExe = new File(chromePath);

        if (chromeExe.exists()) {
            ChromeOptions options = new ChromeOptions();
            options.setBinary(chromePath);
            options.addArguments("--headless=new");
            options.addArguments("--disable-gpu");
            options.addArguments("--no-sandbox");
            options.addArguments("--disable-dev-shm-usage");
            options.addArguments("--window-size=1440,900");
            options.addArguments("--remote-allow-origins=*");
            driver = new ChromeDriver(options);
        } else {
            EdgeOptions edgeOptions = new EdgeOptions();
            edgeOptions.addArguments("--headless=new");
            edgeOptions.addArguments("--disable-gpu");
            edgeOptions.addArguments("--no-sandbox");
            edgeOptions.addArguments("--window-size=1440,900");
            edgeOptions.addArguments("--remote-allow-origins=*");
            driver = new EdgeDriver(edgeOptions);
        }

        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(6));
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(20));
    }

    @AfterEach
    public void tearDownWebDriver() {
        if (driver != null) {
            try {
                driver.quit();
            } catch (Exception ignored) {
            }
        }
    }

    public WebDriver getDriver() {
        return driver;
    }

    protected String getBaseUrl() {
        return "http://localhost:" + port;
    }

    protected void navigateTo(String relativePath) {
        driver.get(getBaseUrl() + relativePath);
    }

    protected void clickElement(WebElement element) {
        try {
            ((JavascriptExecutor) driver).executeScript(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element);
            Thread.sleep(150);
            element.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", element);
        }
    }
}

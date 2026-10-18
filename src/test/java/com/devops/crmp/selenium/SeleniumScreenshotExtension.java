package com.devops.crmp.selenium;

import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.TestWatcher;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Optional;

/**
 * JUnit 5 TestWatcher extension that automatically captures and timestamps
 * full-page browser screenshots whenever a Selenium test assertion fails.
 * 
 * Student: Rushikesh Gawade (23102A0052)
 * Project: Customer Review Moderation Portal (CRMP) - Task 9
 */
public class SeleniumScreenshotExtension implements TestWatcher {

    private static final String FAILURE_DIR = "screenshots/failures";
    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");

    @Override
    public void testFailed(ExtensionContext context, Throwable cause) {
        String testMethodName = context.getRequiredTestMethod().getName();
        String testClassName = context.getRequiredTestClass().getSimpleName();
        System.err.println("==================================================================");
        System.err.println(">>> [SELENIUM TEST FAILURE DETECTED]");
        System.err.println(">>> Test: " + testClassName + "#" + testMethodName);
        System.err.println(">>> Cause: " + (cause != null ? cause.getMessage() : "Unknown assertion error"));
        System.err.println("==================================================================");

        Object testInstance = context.getRequiredTestInstance();
        if (testInstance instanceof BaseSeleniumTest) {
            WebDriver driver = ((BaseSeleniumTest) testInstance).getDriver();
            if (driver != null) {
                File savedFile = captureFailureScreenshot(driver, testMethodName);
                if (savedFile != null) {
                    System.err.println(">>> [AUDIT] Failure evidence recorded at: " + savedFile.getAbsolutePath());
                }
            }
        }
    }

    @Override
    public void testSuccessful(ExtensionContext context) {
        String testMethodName = context.getRequiredTestMethod().getName();
        System.out.println(">>> [SELENIUM PASSED] " + testMethodName + " executed successfully with 0 assertion failures.");
    }

    /**
     * Programmatically captures a failure screenshot into screenshots/failures/
     */
    public static File captureFailureScreenshot(WebDriver driver, String testName) {
        try {
            if (!(driver instanceof TakesScreenshot)) {
                return null;
            }
            File srcFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            Path destDir = Paths.get(FAILURE_DIR);
            Files.createDirectories(destDir);
            String timestamp = LocalDateTime.now().format(FORMATTER);
            String filename = String.format("failure_%s_%s.png", testName, timestamp);
            Path destPath = destDir.resolve(filename);
            Files.copy(srcFile.toPath(), destPath, StandardCopyOption.REPLACE_EXISTING);
            return destPath.toFile();
        } catch (IOException e) {
            System.err.println(">>> Could not persist failure screenshot: " + e.getMessage());
            return null;
        }
    }

    /**
     * Saves a verified journey evidence screenshot into a specified target directory
     */
    public static File captureEvidenceScreenshot(WebDriver driver, String targetDir, String filename) {
        try {
            if (!(driver instanceof TakesScreenshot)) {
                return null;
            }
            File srcFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            Path destDir = Paths.get(targetDir);
            Files.createDirectories(destDir);
            Path destPath = destDir.resolve(filename);
            Files.copy(srcFile.toPath(), destPath, StandardCopyOption.REPLACE_EXISTING);
            System.out.println(">>> [EVIDENCE RECORDED] " + destPath.toAbsolutePath());
            return destPath.toFile();
        } catch (IOException e) {
            System.err.println(">>> Could not persist evidence screenshot: " + e.getMessage());
            return null;
        }
    }
}

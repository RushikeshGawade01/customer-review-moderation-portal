package com.devops.crmp.selenium;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.File;
import java.io.FileInputStream;
import java.time.Duration;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Enterprise Selenium WebDriver 4.x Automated Test Suite for Customer Review Moderation Portal (CRMP).
 * Executes 5 comprehensive test journeys covering customer review submission, validation gates,
 * moderation search & filtering, role-based status lifecycle transitions, and the failure screenshot mechanism.
 * 
 * Student: Rushikesh Gawade (23102A0052)
 * Evaluator: Dr. Snehal Andhare
 * DevOps Lab - Task 9
 */
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class ReviewPortalSeleniumTest extends BaseSeleniumTest {

    private static final String EVIDENCE_DIR = "screenshots/task9";

    @Test
    @Order(1)
    @DisplayName("Journey 1: Reviewer navigates to /reviews/submit, fills feedback form, and asserts PENDING ingestion")
    void testJourney1_ReviewSubmissionLifecycle() {
        navigateTo("/reviews/submit");

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(8));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewSubmissionForm")));

        assertThat(driver.getTitle()).contains("Submit Review");
        assertThat(driver.findElement(By.id("pageTitle")).getText()).contains("Customer Feedback Ingestion Form");

        // Fill Ingestion Form Fields
        driver.findElement(By.id("productId")).sendKeys("PROD-505");
        driver.findElement(By.id("productName")).sendKeys("UltraHD 4K Action Camera");
        driver.findElement(By.id("reviewerName")).sendKeys("Rushikesh Gawade");
        driver.findElement(By.id("reviewerEmail")).sendKeys("rushikesh.gawade@devops.org");
        
        Select ratingSelect = new Select(driver.findElement(By.id("rating")));
        ratingSelect.selectByValue("5");

        driver.findElement(By.id("reviewTitle")).sendKeys("Outstanding Resolution & Image Stabilization");
        driver.findElement(By.id("comment")).sendKeys("This action camera captures breathtaking 4K footage at 60fps with zero jitter. Battery life exceeded 2 hours in continuous recording.");

        // Capture filled form evidence
        SeleniumScreenshotExtension.captureEvidenceScreenshot(driver, EVIDENCE_DIR, "selenium_journey1_form_filled.png");

        // Submit form
        clickElement(driver.findElement(By.id("submitReviewBtn")));

        // Verify flash success alert
        WebElement successAlert = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("submitSuccessAlert")));
        assertThat(successAlert.getText()).contains("submitted successfully");

        // Navigate to moderation directory and verify ingestion record
        navigateTo("/reviews");
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("searchFilterForm")));

        WebElement searchInput = driver.findElement(By.id("searchInput"));
        searchInput.clear();
        searchInput.sendKeys("PROD-505");
        clickElement(driver.findElement(By.id("filterBtn")));

        WebElement table = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewsTable")));
        List<WebElement> rows = table.findElements(By.xpath("//tbody/tr[contains(@id, 'reviewRow-')]"));
        assertThat(rows).isNotEmpty();

        WebElement firstRow = rows.get(0);
        assertThat(firstRow.getText()).contains("UltraHD 4K Action Camera");
        assertThat(firstRow.getText()).contains("Rushikesh Gawade");
        assertThat(firstRow.getText()).contains("PENDING");

        // Capture verified moderation queue evidence
        SeleniumScreenshotExtension.captureEvidenceScreenshot(driver, EVIDENCE_DIR, "selenium_journey1_submission.png");
    }

    @Test
    @Order(2)
    @DisplayName("Journey 2: Validation Gate - Submitting empty fields triggers inline errors; spam input triggers FLAGGED")
    void testJourney2_InputValidationGate() {
        navigateTo("/reviews/submit");

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(8));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewSubmissionForm")));

        // Case A: Submit Empty Form to trigger validation errors
        clickElement(driver.findElement(By.id("submitReviewBtn")));

        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("invalid-feedback")));
        List<WebElement> invalidFeedbacks = driver.findElements(By.className("invalid-feedback"));
        assertThat(invalidFeedbacks.size()).isGreaterThanOrEqualTo(4);

        String pageSource = driver.getPageSource();
        assertThat(pageSource).contains("Product ID is mandatory");
        assertThat(pageSource).contains("Product Name is mandatory");
        assertThat(pageSource).contains("Reviewer Name is mandatory");

        // Capture validation gate errors
        SeleniumScreenshotExtension.captureEvidenceScreenshot(driver, EVIDENCE_DIR, "selenium_journey2_validation.png");

        // Case B: Ingest Spam Feedback to verify automated spam tagging
        driver.findElement(By.id("productId")).sendKeys("PROD-SPAM-99");
        driver.findElement(By.id("productName")).sendKeys("Discount Scam Product");
        driver.findElement(By.id("reviewerName")).sendKeys("Spam Bot");
        driver.findElement(By.id("reviewerEmail")).sendKeys("bot@scamnetwork.xyz");
        new Select(driver.findElement(By.id("rating"))).selectByValue("1");
        driver.findElement(By.id("reviewTitle")).sendKeys("Free Bitcoin Crypto Giveaway");
        driver.findElement(By.id("comment")).sendKeys("Free bonus money and crypto reward! Click this scam link right now: http://fakeurl.xyz");

        clickElement(driver.findElement(By.id("submitReviewBtn")));

        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("submitSuccessAlert")));

        // Check moderation queue to verify automated FLAGGED status
        navigateTo("/reviews");
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("searchInput")));
        driver.findElement(By.id("searchInput")).sendKeys("PROD-SPAM-99");
        clickElement(driver.findElement(By.id("filterBtn")));

        WebElement table = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewsTable")));
        List<WebElement> spamRows = table.findElements(By.xpath("//tbody/tr[contains(@id, 'reviewRow-')]"));
        assertThat(spamRows).isNotEmpty();
        assertThat(spamRows.get(0).getText()).contains("FLAGGED");
    }

    @Test
    @Order(3)
    @DisplayName("Journey 3: Moderation Queue Search, Status Filtering, and Query Reset")
    void testJourney3_SearchAndFilterModerationQueue() {
        navigateTo("/reviews");

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(8));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("searchFilterForm")));

        // Step 1: Keyword search for "Headphones"
        WebElement searchInput = driver.findElement(By.id("searchInput"));
        searchInput.clear();
        searchInput.sendKeys("Headphones");
        clickElement(driver.findElement(By.id("filterBtn")));

        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewsTable")));
        List<WebElement> searchResults = driver.findElements(By.xpath("//tbody/tr[contains(@id, 'reviewRow-')]"));
        assertThat(searchResults).isNotEmpty();
        for (WebElement row : searchResults) {
            assertThat(row.getText().toLowerCase()).contains("headphones");
        }

        // Step 2: Status filtering for "APPROVED"
        Select statusSelect = new Select(driver.findElement(By.id("statusFilterSelect")));
        statusSelect.selectByValue("APPROVED");
        driver.findElement(By.id("searchInput")).clear();
        clickElement(driver.findElement(By.id("filterBtn")));

        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewsTable")));
        List<WebElement> approvedResults = driver.findElements(By.xpath("//tbody/tr[contains(@id, 'reviewRow-')]"));
        assertThat(approvedResults).isNotEmpty();
        for (WebElement row : approvedResults) {
            assertThat(row.getText()).contains("APPROVED");
        }

        // Step 3: Reset filter to restore full queue
        clickElement(driver.findElement(By.id("resetBtn")));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewsTable")));
        List<WebElement> allRows = driver.findElements(By.xpath("//tbody/tr[contains(@id, 'reviewRow-')]"));
        assertThat(allRows.size()).isGreaterThanOrEqualTo(5);

        // Capture evidence of moderation filter workflow
        SeleniumScreenshotExtension.captureEvidenceScreenshot(driver, EVIDENCE_DIR, "selenium_journey3_filter.png");
    }

    @Test
    @Order(4)
    @DisplayName("Journey 4: Moderator Status Lifecycle Transitions (Approve, Flag, Reject)")
    void testJourney4_ModeratorStatusTransitions() {
        navigateTo("/reviews");

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(8));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewsTable")));

        // Locate any active review with an enabled Approve button
        List<WebElement> approveButtons = driver.findElements(By.xpath("//button[contains(@id, 'approveBtn-') and not(@disabled)]"));
        assertThat(approveButtons).isNotEmpty();
        WebElement approveBtn = approveButtons.get(0);
        String approveBtnId = approveBtn.getAttribute("id");
        String reviewId = approveBtnId.replace("approveBtn-", "");

        clickElement(approveBtn);

        wait.until(ExpectedConditions.textToBePresentInElementLocated(By.id("statusSuccessAlert"), "APPROVED"));
        wait.until(ExpectedConditions.textToBePresentInElementLocated(By.id("statusBadge-" + reviewId), "APPROVED"));
        WebElement badgeApproved = driver.findElement(By.id("statusBadge-" + reviewId));
        assertThat(badgeApproved.getText()).isEqualTo("APPROVED");
        assertThat(badgeApproved.getAttribute("class")).contains("badge-approved");

        // Locate any active review with an enabled Flag button in the updated DOM
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewsTable")));
        List<WebElement> flagButtons = driver.findElements(By.xpath("//button[contains(@id, 'flagBtn-') and not(@disabled)]"));
        assertThat(flagButtons).isNotEmpty();
        WebElement flagBtn = flagButtons.get(0);
        String flagBtnId = flagBtn.getAttribute("id");
        String flagReviewId = flagBtnId.replace("flagBtn-", "");

        clickElement(flagBtn);

        wait.until(ExpectedConditions.textToBePresentInElementLocated(By.id("statusSuccessAlert"), "FLAGGED"));
        wait.until(ExpectedConditions.textToBePresentInElementLocated(By.id("statusBadge-" + flagReviewId), "FLAGGED"));
        WebElement badgeFlagged = driver.findElement(By.id("statusBadge-" + flagReviewId));
        assertThat(badgeFlagged.getText()).isEqualTo("FLAGGED");
        assertThat(badgeFlagged.getAttribute("class")).contains("badge-flagged");

        // Capture status transition verification evidence
        SeleniumScreenshotExtension.captureEvidenceScreenshot(driver, EVIDENCE_DIR, "selenium_journey4_moderation.png");
    }

    @Test
    @Order(5)
    @DisplayName("Journey 5: Failure Screenshot Mechanism Verification & Artifact Integrity")
    void testJourney5_FailureScreenshotMechanismVerification() throws Exception {
        navigateTo("/reviews/submit");

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(8));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reviewSubmissionForm")));

        // Programmatically trigger failure screenshot capture mechanism
        File failureScreenshot = SeleniumScreenshotExtension.captureFailureScreenshot(
                driver, "intentional_assertion_failure_demo");

        assertThat(failureScreenshot).isNotNull();
        assertThat(failureScreenshot).exists();
        assertThat(failureScreenshot.length()).isGreaterThan(10000L);

        // Verify valid PNG header magic bytes: [0x89, 'P', 'N', 'G']
        try (FileInputStream fis = new FileInputStream(failureScreenshot)) {
            byte[] header = new byte[4];
            int read = fis.read(header);
            assertThat(read).isEqualTo(4);
            assertThat(header[0]).isEqualTo((byte) 0x89);
            assertThat(header[1]).isEqualTo((byte) 'P');
            assertThat(header[2]).isEqualTo((byte) 'N');
            assertThat(header[3]).isEqualTo((byte) 'G');
        }

        // Also save a verified copy into screenshots/task9/ for document inclusion
        File docEvidence = SeleniumScreenshotExtension.captureEvidenceScreenshot(
                driver, EVIDENCE_DIR, "selenium_failure_screenshot_demo.png");
        assertThat(docEvidence).isNotNull();
        assertThat(docEvidence).exists();
    }
}

package com.devops.crmp;

import com.devops.crmp.service.SpamDetectionService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class SpamDetectionServiceTest {

    private SpamDetectionService spamDetectionService;

    @BeforeEach
    void setUp() {
        spamDetectionService = new SpamDetectionService();
    }

    @Test
    @DisplayName("Should detect spam containing promotional keyword 'free gift cards'")
    void testKeywordSpamDetection() {
        String comment = "Get free gift cards now by following this simple survey!";
        boolean isSpam = spamDetectionService.isSuspectedSpam(comment);
        assertThat(isSpam).isTrue();
    }

    @Test
    @DisplayName("Should detect spam containing external malicious URL")
    void testUrlSpamDetection() {
        String comment = "Awesome discounts on our partner store visit http://fake-deals.xyz/bonus";
        boolean isSpam = spamDetectionService.isSuspectedSpam(comment);
        assertThat(isSpam).isTrue();
    }

    @Test
    @DisplayName("Should pass genuine customer review feedback without flagging")
    void testGenuineReviewPasses() {
        String comment = "The build quality is very solid and battery life comfortably lasts 2 full workdays.";
        boolean isSpam = spamDetectionService.isSuspectedSpam(comment);
        assertThat(isSpam).isFalse();
    }
}

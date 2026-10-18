package com.devops.crmp;

import com.devops.crmp.model.Review;
import com.devops.crmp.model.ReviewStatus;
import com.devops.crmp.service.ReviewService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class CustomerReviewPortalApplicationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ReviewService reviewService;

    @Test
    @DisplayName("Test 1: Context loads successfully and initial seed data exists")
    void contextLoads() {
        assertThat(reviewService).isNotNull();
        assertThat(reviewService.getAllReviews()).isNotEmpty();
    }

    @Test
    @DisplayName("Test 2: Dashboard / endpoint returns 200 OK and renders KPI cards")
    void testDashboardPage() throws Exception {
        mockMvc.perform(get("/"))
                .andExpect(status().isOk())
                .andExpect(view().name("index"))
                .andExpect(content().string(containsString("Review Operations & Moderation KPI Dashboard")))
                .andExpect(content().string(containsString("Total Reviews")));
    }

    @Test
    @DisplayName("Test 3: Moderation queue /reviews returns 200 OK and table rows")
    void testModerationQueuePage() throws Exception {
        mockMvc.perform(get("/reviews"))
                .andExpect(status().isOk())
                .andExpect(view().name("reviews"))
                .andExpect(content().string(containsString("Customer Review Directory & Moderation Queue")))
                .andExpect(content().string(containsString("PROD-101")));
    }

    @Test
    @DisplayName("Test 4: Submission form /reviews/submit returns 200 OK")
    void testSubmitReviewPage() throws Exception {
        mockMvc.perform(get("/reviews/submit"))
                .andExpect(status().isOk())
                .andExpect(view().name("submit"))
                .andExpect(content().string(containsString("Customer Feedback Ingestion Form")));
    }

    @Test
    @DisplayName("Test 5: Actuator health probe returns UP with HTTP 200")
    void testActuatorHealthProbe() throws Exception {
        mockMvc.perform(get("/actuator/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }

    @Test
    @DisplayName("Test 6: Valid review submission creates pending review and redirects")
    void testValidReviewSubmission() throws Exception {
        mockMvc.perform(post("/reviews/submit")
                        .param("productId", "PROD-201")
                        .param("productName", "Noise Cancelling Earbuds Pro")
                        .param("reviewerName", "Rushikesh Gawade")
                        .param("reviewerEmail", "rushikesh@example.com")
                        .param("rating", "5")
                        .param("reviewTitle", "Excellent Audio Clarity")
                        .param("comment", "Crystal clear sound and deep bass response. Highly recommended for daily travel."))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/reviews/submit"))
                .andExpect(flash().attributeExists("successMessage"));
    }

    @Test
    @DisplayName("Test 7: Moderation state transition to APPROVED")
    void testStatusTransitionToApproved() throws Exception {
        Review review = new Review("PROD-301", "USB-C Multiport Hub", "Rahul Deshmukh", 
                                   "rahul.d@example.com", 4, "Reliable Hub", "All ports operate at USB 3.2 speeds as advertised.");
        Review saved = reviewService.saveReview(review);

        mockMvc.perform(post("/reviews/" + saved.getId() + "/status")
                        .param("status", "APPROVED"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/reviews"))
                .andExpect(flash().attributeExists("statusMessage"));

        Review updated = reviewService.getReviewById(saved.getId()).orElseThrow();
        assertThat(updated.getStatus()).isEqualTo(ReviewStatus.APPROVED);
    }
}

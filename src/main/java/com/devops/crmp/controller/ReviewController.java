package com.devops.crmp.controller;

import com.devops.crmp.model.Review;
import com.devops.crmp.model.ReviewStatus;
import com.devops.crmp.service.ReviewService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;

@Controller
@RequestMapping("/reviews")
public class ReviewController {

    private final ReviewService reviewService;

    @Autowired
    public ReviewController(ReviewService reviewService) {
        this.reviewService = reviewService;
    }

    @GetMapping
    public String viewReviewDirectory(@RequestParam(value = "query", required = false) String query,
                                      @RequestParam(value = "status", required = false, defaultValue = "ALL") String status,
                                      Model model) {
        List<Review> reviews = reviewService.filterReviews(query, status);
        model.addAttribute("reviews", reviews);
        model.addAttribute("currentQuery", query != null ? query : "");
        model.addAttribute("currentStatus", status);
        model.addAttribute("statuses", ReviewStatus.values());
        model.addAttribute("metrics", reviewService.getMetricsSummary());
        return "reviews";
    }

    @GetMapping("/submit")
    public String showSubmissionForm(Model model) {
        if (!model.containsAttribute("review")) {
            model.addAttribute("review", new Review());
        }
        return "submit";
    }

    @PostMapping("/submit")
    public String processReviewSubmission(@Valid @ModelAttribute("review") Review review,
                                          BindingResult bindingResult,
                                          RedirectAttributes redirectAttributes,
                                          Model model) {
        if (bindingResult.hasErrors()) {
            return "submit";
        }

        reviewService.saveReview(review);
        redirectAttributes.addFlashAttribute("successMessage", 
                "Your review for '" + review.getProductName() + "' has been submitted successfully and is awaiting moderation!");
        return "redirect:/reviews/submit";
    }

    @PostMapping("/{id}/status")
    public String updateReviewStatus(@PathVariable("id") Long id,
                                     @RequestParam("status") ReviewStatus status,
                                     RedirectAttributes redirectAttributes) {
        boolean updated = reviewService.updateStatus(id, status);
        if (updated) {
            redirectAttributes.addFlashAttribute("statusMessage", 
                    "Review #" + id + " status successfully updated to " + status + ".");
        } else {
            redirectAttributes.addFlashAttribute("errorMessage", 
                    "Failed to update status for Review #" + id + ".");
        }
        return "redirect:/reviews";
    }

    // REST APIs for automated verification
    @GetMapping("/api/all")
    @ResponseBody
    public ResponseEntity<List<Review>> getAllReviewsApi() {
        return ResponseEntity.ok(reviewService.getAllReviews());
    }

    @PostMapping("/api/submit")
    @ResponseBody
    public ResponseEntity<?> submitReviewApi(@Valid @RequestBody Review review, BindingResult result) {
        if (result.hasErrors()) {
            return ResponseEntity.badRequest().body(result.getAllErrors());
        }
        Review saved = reviewService.saveReview(review);
        return ResponseEntity.ok(saved);
    }
}

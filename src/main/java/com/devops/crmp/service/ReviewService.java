package com.devops.crmp.service;

import com.devops.crmp.model.Review;
import com.devops.crmp.model.ReviewStatus;
import com.devops.crmp.repository.ReviewRepository;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Service
public class ReviewService {

    private final ReviewRepository reviewRepository;

    @Autowired
    public ReviewService(ReviewRepository reviewRepository) {
        this.reviewRepository = reviewRepository;
    }

    @PostConstruct
    public void seedInitialData() {
        if (reviewRepository.count() == 0) {
            Review r1 = new Review("PROD-101", "Ultra Wireless Noise-Cancelling Headphones", 
                                   "Ananya Sharma", "ananya.sharma@example.com", 5, 
                                   "Outstanding Sound Quality & ANC", 
                                   "These headphones exceeded all expectations. Battery life lasted over 36 hours on a single charge and active noise cancellation is top notch.");
            r1.setStatus(ReviewStatus.APPROVED);

            Review r2 = new Review("PROD-102", "Ergonomic Mechanical Keyboard RGB", 
                                   "Vikram Malhotra", "vikram.m@example.com", 4, 
                                   "Great Tactile Feedback, Slightly Loud", 
                                   "The tactile Brown switches feel amazing for day-long coding. RGB lighting customization works seamlessly under Linux and Windows.");
            r2.setStatus(ReviewStatus.PENDING);

            Review r3 = new Review("PROD-103", "4K Ultra-HD 27-inch Gaming Monitor", 
                                   "Pooja Deshmukh", "pooja.d@example.com", 5, 
                                   "Crisp IPS Panel with 144Hz Refresh Rate", 
                                   "Color calibration out of the box was spot on. HDR400 brings games to life with vibrant contrast.");
            r3.setStatus(ReviewStatus.APPROVED);

            Review r4 = new Review("PROD-104", "Smart Fitness Tracker Band 7", 
                                   "Bot_Promo99", "free.deals.bot@spamsite.xyz", 1, 
                                   "WIN FREE GIFT CARDS CLICK HERE http://spam.ru", 
                                   "Get free promotional vouchers and prizes instantly by visiting our sponsor link! Cheap deals 24/7!");
            r4.setStatus(ReviewStatus.REJECTED);

            Review r5 = new Review("PROD-105", "Fast Charging 65W GaN USB-C Charger", 
                                   "Siddharth Patil", "sid.patil@example.com", 3, 
                                   "Decent Charger, Heats Up Under Full Load", 
                                   "Charges laptop and phone quickly simultaneously, but the brick gets noticeably hot after 45 minutes of continuous 65W output.");
            r5.setStatus(ReviewStatus.FLAGGED);

            reviewRepository.saveAll(Arrays.asList(r1, r2, r3, r4, r5));
        }
    }

    public List<Review> getAllReviews() {
        return reviewRepository.findAll();
    }

    public List<Review> filterReviews(String query, String status) {
        boolean hasQuery = (query != null && !query.trim().isEmpty());
        boolean hasStatus = (status != null && !status.trim().isEmpty() && !status.equalsIgnoreCase("ALL"));

        if (hasQuery && hasStatus) {
            ReviewStatus st = ReviewStatus.valueOf(status.toUpperCase());
            return reviewRepository.searchReviewsByStatus(query.trim(), st);
        } else if (hasQuery) {
            return reviewRepository.searchReviews(query.trim());
        } else if (hasStatus) {
            ReviewStatus st = ReviewStatus.valueOf(status.toUpperCase());
            return reviewRepository.findByStatus(st);
        } else {
            return reviewRepository.findAll();
        }
    }

    public Optional<Review> getReviewById(Long id) {
        return reviewRepository.findById(id);
    }

    @Transactional
    public Review saveReview(Review review) {
        if (review.getStatus() == null) {
            review.setStatus(ReviewStatus.PENDING);
        }
        return reviewRepository.save(review);
    }

    @Transactional
    public boolean updateStatus(Long id, ReviewStatus newStatus) {
        Optional<Review> opt = reviewRepository.findById(id);
        if (opt.isPresent()) {
            Review r = opt.get();
            r.setStatus(newStatus);
            reviewRepository.save(r);
            return true;
        }
        return false;
    }

    public Map<String, Object> getMetricsSummary() {
        List<Review> all = reviewRepository.findAll();
        long total = all.size();
        long pending = all.stream().filter(r -> r.getStatus() == ReviewStatus.PENDING).count();
        long approved = all.stream().filter(r -> r.getStatus() == ReviewStatus.APPROVED).count();
        long rejected = all.stream().filter(r -> r.getStatus() == ReviewStatus.REJECTED).count();
        long flagged = all.stream().filter(r -> r.getStatus() == ReviewStatus.FLAGGED).count();

        double avgRating = all.stream()
                .filter(r -> r.getStatus() == ReviewStatus.APPROVED)
                .mapToInt(Review::getRating)
                .average()
                .orElse(0.0);

        Map<String, Object> metrics = new HashMap<>();
        metrics.put("totalReviews", total);
        metrics.put("pendingReviews", pending);
        metrics.put("approvedReviews", approved);
        metrics.put("rejectedReviews", rejected);
        metrics.put("flaggedReviews", flagged);
        metrics.put("averageRating", String.format(Locale.US, "%.1f", avgRating));
        return metrics;
    }
}

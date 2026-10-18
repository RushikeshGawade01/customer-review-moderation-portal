package com.devops.crmp.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "reviews")
public class Review {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Product ID is mandatory")
    @Column(nullable = false)
    private String productId;

    @NotBlank(message = "Product Name is mandatory")
    @Column(nullable = false)
    private String productName;

    @NotBlank(message = "Reviewer Name is mandatory")
    @Column(nullable = false)
    private String reviewerName;

    @Email(message = "Please provide a valid email address")
    @NotBlank(message = "Reviewer Email is mandatory")
    @Column(nullable = false)
    private String reviewerEmail;

    @NotNull(message = "Rating is mandatory")
    @Min(value = 1, message = "Rating must be between 1 and 5 stars")
    @Max(value = 5, message = "Rating must be between 1 and 5 stars")
    @Column(nullable = false)
    private Integer rating;

    @NotBlank(message = "Review Title is mandatory")
    @Size(min = 3, max = 120, message = "Title must be between 3 and 120 characters")
    @Column(nullable = false)
    private String reviewTitle;

    @NotBlank(message = "Review Comment is mandatory")
    @Size(min = 10, max = 2000, message = "Review comment must be at least 10 characters")
    @Column(nullable = false, length = 2000)
    private String comment;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ReviewStatus status = ReviewStatus.PENDING;

    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(length = 1000)
    private String moderatorNotes;

    @Column
    private LocalDateTime moderatedAt;

    @Column
    private String moderatedBy;

    public Review() {
    }

    public Review(String productId, String productName, String reviewerName, String reviewerEmail, 
                  Integer rating, String reviewTitle, String comment) {
        this.productId = productId;
        this.productName = productName;
        this.reviewerName = reviewerName;
        this.reviewerEmail = reviewerEmail;
        this.rating = rating;
        this.reviewTitle = reviewTitle;
        this.comment = comment;
        this.status = ReviewStatus.PENDING;
        this.createdAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getProductId() {
        return productId;
    }

    public void setProductId(String productId) {
        this.productId = productId;
    }

    public String getProductName() {
        return productName;
    }

    public void setProductName(String productName) {
        this.productName = productName;
    }

    public String getReviewerName() {
        return reviewerName;
    }

    public void setReviewerName(String reviewerName) {
        this.reviewerName = reviewerName;
    }

    public String getReviewerEmail() {
        return reviewerEmail;
    }

    public void setReviewerEmail(String reviewerEmail) {
        this.reviewerEmail = reviewerEmail;
    }

    public Integer getRating() {
        return rating;
    }

    public void setRating(Integer rating) {
        this.rating = rating;
    }

    public String getReviewTitle() {
        return reviewTitle;
    }

    public void setReviewTitle(String reviewTitle) {
        this.reviewTitle = reviewTitle;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public ReviewStatus getStatus() {
        return status;
    }

    public void setStatus(ReviewStatus status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public String getModeratorNotes() {
        return moderatorNotes;
    }

    public void setModeratorNotes(String moderatorNotes) {
        this.moderatorNotes = moderatorNotes;
    }

    public LocalDateTime getModeratedAt() {
        return moderatedAt;
    }

    public void setModeratedAt(LocalDateTime moderatedAt) {
        this.moderatedAt = moderatedAt;
    }

    public String getModeratedBy() {
        return moderatedBy;
    }

    public void setModeratedBy(String moderatedBy) {
        this.moderatedBy = moderatedBy;
    }
}

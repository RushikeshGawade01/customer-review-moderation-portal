package com.devops.crmp.repository;

import com.devops.crmp.model.Review;
import com.devops.crmp.model.ReviewStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {

    List<Review> findByStatus(ReviewStatus status);

    @Query("SELECT r FROM Review r WHERE " +
           "LOWER(r.productId) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(r.productName) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(r.reviewerName) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(r.reviewTitle) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(r.comment) LIKE LOWER(CONCAT('%', :query, '%'))")
    List<Review> searchReviews(@Param("query") String query);

    @Query("SELECT r FROM Review r WHERE r.status = :status AND (" +
           "LOWER(r.productId) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(r.productName) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(r.reviewerName) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(r.reviewTitle) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(r.comment) LIKE LOWER(CONCAT('%', :query, '%')))")
    List<Review> searchReviewsByStatus(@Param("query") String query, @Param("status") ReviewStatus status);

    long countByStatus(ReviewStatus status);
}

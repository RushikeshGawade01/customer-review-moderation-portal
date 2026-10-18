package com.devops.crmp.controller;

import com.devops.crmp.service.ReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class DashboardController {

    private final ReviewService reviewService;

    @Autowired
    public DashboardController(ReviewService reviewService) {
        this.reviewService = reviewService;
    }

    @GetMapping({"/", "/dashboard"})
    public String showDashboard(Model model) {
        model.addAttribute("metrics", reviewService.getMetricsSummary());
        model.addAttribute("recentReviews", reviewService.getAllReviews());
        return "index";
    }
}

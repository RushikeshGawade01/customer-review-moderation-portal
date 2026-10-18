package com.devops.crmp.service;

import org.springframework.stereotype.Service;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

@Service
public class SpamDetectionService {

    private static final List<String> SPAM_KEYWORDS = Arrays.asList(
            "free gift cards",
            "click here",
            "http://",
            "https://",
            "free deals",
            "claim prize",
            "earn cash fast",
            "casino",
            "win money"
    );

    private static final Pattern URL_PATTERN = Pattern.compile("https?://[\\w.-]+(?:\\.[\\w\\.-]+)+[/\\w\\._~:?#\\[\\]@!\\$&'\\(\\)\\*\\+,;=.]*", Pattern.CASE_INSENSITIVE);

    /**
     * Evaluates comment text against spam heuristics.
     * Returns true if suspicious keywords or external hyperlinks are detected.
     */
    public boolean isSuspectedSpam(String content) {
        if (content == null || content.trim().isEmpty()) {
            return false;
        }

        String lower = content.toLowerCase();
        for (String keyword : SPAM_KEYWORDS) {
            if (lower.contains(keyword)) {
                return true;
            }
        }

        return URL_PATTERN.matcher(content).find();
    }
}

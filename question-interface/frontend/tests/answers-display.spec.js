import { test, expect } from '@playwright/test';

test('verify answers are displayed', async ({ page }) => {
  const logs = [];

  page.on('console', msg => {
    logs.push(`[${msg.type()}] ${msg.text()}`);
  });

  await page.goto('http://localhost:5173');
  await page.waitForTimeout(5000);

  // Check if questions are loaded
  const questionElements = page.locator('h3');
  const count = await questionElements.count();
  console.log(`Found ${count} questions`);

  // Check for answer indicators
  const answeredQuestions = page.locator('text=/📝/');
  const answeredCount = await answeredQuestions.count();
  console.log(`Found ${answeredCount} answered questions`);

  // Click "Show Answer" buttons to reveal answers
  const showButtons = page.locator('button:has-text("Show Answer")');
  const buttonCount = await showButtons.count();
  console.log(`Found ${buttonCount} "Show Answer" buttons`);

  if (buttonCount > 0) {
    // Click the first few show answer buttons
    const buttonsToClick = Math.min(buttonCount, 3);
    for (let i = 0; i < buttonsToClick; i++) {
      await showButtons.nth(i).click();
      await page.waitForTimeout(500); // Wait for animation
    }
  }

  // Now check if markdown content is rendered
  const answerSections = page.locator('text=/Answer:/');
  const answerCount = await answerSections.count();
  console.log(`Found ${answerCount} answer sections after clicking buttons`);

  // Verify at least some answers are displayed
  expect(answerCount).toBeGreaterThan(0);

  console.log('Console logs:', logs.slice(0, 10));
});
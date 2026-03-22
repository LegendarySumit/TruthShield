import { test, expect } from '@playwright/test';

test('submits text and renders prediction result with captcha bypass', async ({ page }) => {
  await page.route('**/api/v1/predict', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        prediction: 'Real',
        confidence: 0.91,
        explanation: '[AI Fact-Check] Source-attributed, measured language and consistent claims.',
        model_version: 'v3',
      }),
    });
  });

  await page.goto('/');

  const textarea = page.getByPlaceholder(/Paste your news article here/i);
  await textarea.fill(
    'The Senate voted 67-33 to approve the Infrastructure Investment Act, allocating funds for bridge and road repairs across several states with source attribution and measured language.'
  );

  await page.getByRole('button', { name: /Verify Now/i }).click();

  await expect(page.getByText('Verification Result')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Real' })).toBeVisible();
  await expect(page.getByText('AI Analysis')).toBeVisible();
  await expect(page.getByText(/Source-attributed, measured language/i)).toBeVisible();
});

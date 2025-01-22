"""Report generation module for branch protection status."""
from datetime import datetime
from fpdf import FPDF
import os
from typing import Dict, List

from .logger import logger

class ProtectionReport(FPDF):
    def header(self):
        # Logo (if you have one)
        # self.image('logo.png', 10, 8, 33)
        
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        
        # Title
        self.cell(0, 10, 'GitHub Branch Protection Report', 0, 1, 'C')
        
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)
        
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

def generate_protection_report(verification_results: List[Dict], output_dir: str = "reports") -> str:
    """Generate a PDF report of branch protection status."""
    try:
        # Create reports directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize PDF
        pdf = ProtectionReport()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # Report metadata
        now = datetime.now()
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 5, f'Generated: {now.strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
        pdf.ln(5)
        
        # Summary section
        total_repos = len(verification_results)
        compliant_repos = sum(1 for r in verification_results if r['status'])
        
        pdf.chapter_title('Executive Summary')
        summary = (
            f'Total Repositories Scanned: {total_repos}\n'
            f'Compliant Repositories: {compliant_repos}\n'
            f'Non-compliant Repositories: {total_repos - compliant_repos}\n'
            f'Compliance Rate: {(compliant_repos/total_repos)*100:.1f}%'
        )
        pdf.chapter_body(summary)
        
        # Detailed Results
        pdf.add_page()
        pdf.chapter_title('Detailed Results')
        
        for result in verification_results:
            repo_name = result['repository']
            status = result['status']
            issues = result.get('issues', [])
            default_branch = result.get('default_branch', 'unknown')
            
            # Repository header
            pdf.set_font('Arial', 'B', 11)
            status_color = (0, 200, 0) if status else (200, 0, 0)
            pdf.set_text_color(*status_color)
            pdf.cell(0, 6, f"Repository: {repo_name}", 0, 1)
            pdf.set_text_color(0, 0, 0)
            
            # Repository details
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 5, f"Default Branch: {default_branch}", 0, 1)
            # Using [PASS] and [FAIL] instead of Unicode symbols
            status_text = '[PASS] Compliant' if status else '[FAIL] Non-compliant'
            pdf.cell(0, 5, f"Status: {status_text}", 0, 1)
            
            if not status and issues:
                pdf.ln(2)
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 5, "Issues Found:", 0, 1)
                pdf.set_font('Arial', '', 10)
                for issue in issues:
                    pdf.cell(0, 5, f"- {issue}", 0, 1)  # Using hyphen instead of bullet point
            
            pdf.ln(5)
        
        # Recommendations
        pdf.add_page()
        pdf.chapter_title('Recommendations')
        recommendations = (
            "1. Ensure all repositories have branch protection rules enabled\n\n"
            "2. Required settings for optimal security:\n"
            "   - Require pull request reviews\n"
            "   - Require at least 1 approving review\n"
            "   - Dismiss stale pull request approvals\n"
            "   - Require status checks to pass\n"
            "   - Enforce for administrators\n"
            "   - Prevent force pushes\n"
            "   - Prevent branch deletions\n\n"
            "3. Regular audits of branch protection settings are recommended"
        )
        pdf.chapter_body(recommendations)
        
        # Save the report
        filename = f"branch_protection_report_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(output_dir, filename)
        pdf.output(filepath, 'F')  # Added 'F' parameter for binary write mode
        
        logger.info(f"Generated protection report: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Failed to generate protection report: {str(e)}")
        raise 
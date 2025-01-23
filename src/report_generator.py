"""Report generation module for branch protection status."""
from datetime import datetime
from fpdf import FPDF
import os
from typing import Dict, List

from .logger import logger

class ProtectionReport(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Title
        self.cell(0, 10, 'Branch Protection Audit Report', 0, 1, 'C')
        # Line break
        self.ln(10)
        
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)
        
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()
        
    def add_repository_section(self, repo_data: Dict):
        status = '[PASS]' if repo_data['status'] else '[FAIL]'
        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, f"{status} {repo_data['name']}", 0, 1, 'L')
        
        if not repo_data['status']:
            self.set_font('Arial', '', 10)
            for issue in repo_data['issues']:
                self.cell(10)
                self.cell(0, 8, f"- {issue}", 0, 1, 'L')
        self.ln(4)

def generate_protection_report(results: List[Dict]) -> str:
    """Generate PDF report of protection status."""
    try:
        # Create output directory if it doesn't exist
        output_dir = 'reports'
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize PDF
        pdf = ProtectionReport()
        pdf.add_page()
        
        # Add timestamp
        now = datetime.now()
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'R')
        pdf.ln(4)
        
        # Add summary
        total = len(results)
        passed = sum(1 for r in results if r['status'])
        pdf.chapter_title('Summary')
        summary = (
            f"Total Repositories: {total}\n"
            f"Properly Protected: {passed}\n"
            f"Need Attention: {total - passed}"
        )
        pdf.chapter_body(summary)
        
        # Add detailed results
        pdf.chapter_title('Detailed Results')
        for repo in results:
            pdf.add_repository_section(repo)
        
        # Add recommendations if needed
        if total - passed > 0:
            pdf.chapter_title('Recommendations')
            recommendations = (
                "1. Review failed repositories and their specific issues\n"
                "2. Ensure proper permissions are set for the GitHub token\n"
                "3. Consider enabling additional protection features\n"
                "4. Re-run verification after addressing issues"
            )
            pdf.chapter_body(recommendations)
        
        # Save the report
        filename = f"branch_protection_report_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(output_dir, filename)
        pdf.output(filepath, 'F')
        
        logger.info(f"Generated protection report: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Failed to generate protection report: {str(e)}")
        raise 
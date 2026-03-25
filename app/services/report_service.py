from app.models.report import Report
from app.repositories.report_repository import ReportRespository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from datetime import datetime

class ReportService:

    @staticmethod
    def report_post(reporter_id: int, post_id: int, reason: str) -> Report:
        if not reason or not reason.strip():
            raise ValueError("A reason must be provided.")
        
        reporter = UserRepository.get_by_id(reporter_id)

        if not reporter or not reporter.is_active:
            raise ValueError("Reporter not found or not active.")
        
        post = PostRepository.get_by_id(post_id)

        if not post or not post.is_active:
            raise ValueError("Post not found or already removed.")
        
        if post.author_id == reporter_id:
            raise ValueError("You can't report your own post.")
        
        if ReportRespository.already_reported(reporter_id = reporter_id, post_id = post_id):
            raise ValueError("You already reported this post.")
        
        report = Report(
            reporter_id=reporter_id,
            reported_post_id=post_id,
            reason=reason.strip()
        )

        return ReportRespository.create(report)
    
    @staticmethod
    def report_user(reporter_id: int, target_user_id: int, reason: str) -> Report:
        if not reason or not reason.strip():
            raise ValueError("A reason must be provided.")
        
        if reporter_id == target_user_id:
            raise ValueError("You can't report yourself.")
        
        reporter = UserRepository.get_by_id(reporter_id)
        target = UserRepository.get_by_id(target_user_id)

        if not reporter:
            raise ValueError("Reporter not found.")
        
        if not target:
            raise ValueError("Target user not found.")

        if ReportRespository.already_reported(reporter_id = reporter_id, user_id = target_user_id):
            raise ValueError("You already reported this user.")

        report = Report(
            reporter_id = reporter_id,
            reported_user_id = target_user_id,
            reason = reason.strip()
        )

        return ReportRespository.create(report)
    
    @staticmethod
    def get_pending_reports(requester_id = int) -> list:
        requester = UserRepository.get_by_id(requester_id)

        if not requester or requester.role not in ['moderator', 'admin']:
            raise PermissionError("Access Denied! Only moderator and admins can view reports.")
        
        reports = ReportRespository.get_pending()

        return[r.to_dict() for r in reports]
    
    @staticmethod
    def get_all_reports(requester_id: int) -> list:
        requester = UserRepository.get_by_id(requester_id)

        if not requester or requester.role != 'admin':
            raise PermissionError("Access Denied! Only admins can view all reports.")
        
        reports = ReportRespository.get_all()

        return[r.to_dict() for r in reports]

    @staticmethod
    def review_report(report_id: int, requester_id: int, action: str) -> dict:
        requester = UserRepository.get_by_id(requester_id)

        if not requester or requester.role not in ['admin', 'moderator']:
            raise PermissionError("Access Denied! Only admins and moderators can review reports.")
        
        report = ReportRespository.get_by_id(report_id)

        if not report:
            raise ValueError("Report not found.")
        
        if report.status != 'pending':
            raise ValueError(f"This report is already {report.status}.")
        
        if action not in ['dismiss', 'resolve']:
            raise ValueError("Invalid action. Use 'dismiss' or 'resolve'.")
        
        report.status = 'reviewed' if action == 'resolve' else 'dismissed'

        report.reviewed_at = datetime.utcnow()
        report.reviewed_by = requester_id

        ReportRespository.update(report)

        return {"message": f"Report {report_id} has been {report.status}.", "report": report.to_dict()}
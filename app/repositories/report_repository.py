from app import db
from app.models.report import Report

class ReportRespository:
    @staticmethod
    def create(report: Report) -> Report:
        db.session.add(report)
        db.session.commit()
        return report
    
    @staticmethod
    def get_by_id(report_id: int) -> Report:
        return Report.query.get(report_id)
    
    @staticmethod
    def get_all_pending() -> list[Report]:
        return Report.query.filter_by(status='pending').order_by(Report.created_at.desc()).all()
    
    @staticmethod
    def get_all() -> list[Report]:
        return Report.query.order_by(Report.created_at.desc()).all()
    
    @staticmethod
    def update(report: Report) -> Report:
        db.session.commit()
        return report
    
    @staticmethod
    def already_reported(reporter_id: int, post_id: int = None, user_id: int = None) -> bool:
        query = Report.query.filter_by(reporter_id=reporter_id)
        
        if post_id:
            query = query.filter_by(reporter_id = reporter_id)

        if user_id:
            query = query.filter_by(reported_post_id = post_id)
        
        return query.first() is not None
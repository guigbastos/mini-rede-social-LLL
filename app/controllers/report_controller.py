from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.report_service import ReportService

report_bp = Blueprint('report_bp', __name__, url_prefix='/reports')

@report_bp.route('/posts/<int:post_id>', methods=['POST'])
@jwt_required()
def report_post(post_id):
    """
    ---
    tags:
       - Reports
    security:
      - Bearer: []
    summary: ID of a post to report.
    parameters:
       - in: path
         name: post_id
         type: integer
         required: true
         description: ID of the post to report
       - in: body
         name: body
         required: true
         schema:
           type: object
           required:
             - reason
           properties:
             reason:
               type: string
               example: "This post contains hate speech."
    responses:
       201:
        description: Report submitted successfully
       400:
        description: Validation error (e.g., missing reason, already reported, own post)
       401:
        description: Missing or invalid token
       500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data or not data.get('reason'):
        return jsonify({"error": "A reason must be provided."}), 400
    
    try:
        report = ReportService.report_post(
            reporter_id=current_user_id,
            post_id=post_id,
            reason=data['reason']
        )
        return jsonify({"message": "Reported submitted successfully!", "report_id": report.id}), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500
    
@report_bp.route('/users/<int:user_id>', methods=['POST'])
@jwt_required()
def report_user(user_id):
    """
    ---
    tags:
       - Reports
    security:
      - Bearer: []
    summary: ID of the user to report.
    parameters:
       - in: path
         name: user_id
         type: integer
         required: true
         description: ID of the user to report
       - in: body
         name: body
         required: true
         schema:
           type: object
           required:
             - reason
           properties:
             reason:
               type: string
               example: "This user is abusive."
    responses:
       201:
        description: Report submitted successfully
       400:
        description: Validation error (e.g. already reported, self-report)
       401:
        description: Missing or invalid token
       500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data or not data.get('reason'):
        return jsonify({"error": "A reason must be provided."}), 400
    
    try:
        report = ReportService.report_user(
            reporter_id=current_user_id,
            target_user_id=user_id,
            reason=data['reason']
        )
        return jsonify({"message": "Report submitted succesfully.", "report_id": report.id}), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
    
@report_bp.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_reports():
    """
    ---
    tags:
       - Reports
    security:
      - Bearer: []
    summary: (Moderator/Admin) List all pending reports.
    responses:
       200:
        description: Pending reports retrieved successfully
       401:
        description: Missing or invalid token
       403:
        description: Access denied.
       500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())

    try:
        reports = ReportService.get_pending_reports(current_user_id)
        return jsonify(reports), 200
    
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500

@report_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_reports():
    """
    ---
    tags:
       - Reports
    security:
      - Bearer: []
    summary: (Admin only) List all reports including reviewed and dismissed.
    responses:
       200:
        description: All reports retrieved successfully
       401:
        description: Missing or invalid token
       403:
        description: Access denied
       500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())

    try:
        reports = ReportService.get_all_reports(current_user_id)
        return jsonify(reports), 200
    
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify ({"error": "An internal server error occurred."})
    
@report_bp.route('/<int:report_id>/review', methods=['POST'])
@jwt_required()
def review_report(report_id):
    """
    ---
    tags:
       - Reports
    security:
      - Bearer: []
    summary: (Moderator/Admin) Review a pending report.
    parameters:
       - in: path
         name: report_id
         type: integer
         required: true
       - in: body
         name: body
         required: true
         schema:
           type: object
           required:
             - action
           properties:
             action:
               type: string
               enum: [dismiss, resolve]
               example: "resolve"
    responses:
       200:
        description: Report reviewed successfully
       400:
        description: Validation error (e.g., invalid action, already reviewed)
       401:
        description: Missing or invalid token
       500:
        description: Internal server error
    """
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data or not data.get('action'):
        return jsonify({"error": "An action ('dismiss' or 'resolve') must be provided."}), 400
    
    try:
        result = ReportService.review_report(
            report_id=report_id,
            requester_id=current_user_id,
            action=data['action']
        )
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({"error": "An internal server error occurred."}), 500
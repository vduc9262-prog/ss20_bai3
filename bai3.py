

import logging

matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed"
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
]

def render_matches(list):

    print("--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    print(f"{'Mã Trận':<10} | {'đội a ':<10} | {'đội b':<10} | {'tỷ số ':<10} | {'trạng thái':<10} | ")
    print("-" * 70)
    for mat in list:
        print("{match_id:<10} | {team_a:<10} | {team_b:<10} | {score_a}-{score_b:<8} | {status:<10} |".format_map(mat))

    print()
    if list == []:
        print("danh sách trống !!!!")


def add_match(list):

    print("--- THÊM TRẬN ĐẤU MỚI ---")

    match_id = input("Nhập mã trận đấu: ").strip()

    if not match_id:
        print("Mã trận đấu không được để trống.")
        logging.warning("Người dùng đã cố gắng thêm một trận đấu với ID trận đấu trống")
        return

    for match in list:
        if match["match_id"] == match_id:
            print(f"Lỗi: Mã trận đấu {match_id} đã tồn tại")
            logging.warning(f"Mã định danh trận đấu {match_id} đã tồn tại")
            return

    team_a = input("Nhập tên Đội A: ").strip()
    team_b = input("Nhập tên Đội B: ").strip()

    if not team_a or not team_b:
        print("Tên đội không được để trống.")
        logging.warning("Người dùng đã cố gắng thêm một trận đấu với tên đội trống")
        return

    list.append({
        "match_id": match_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    })

    print(f"thành công: Đã thêm trận đấu {match_id}.")
    logging.info(f"trận đấu {match_id} đã được thêm thành công")


def input_score(team_name):

    while True:
        try:
            score = int(input(f"nhập điểm {team_name}: "))
            if score < 0:
                print("điểm số phải lớn hơn hoặc bằng 0.")
                logging.error(f"đã phát hiện điểm số âm được nhập vào:{score}")
                continue
            return score

        except ValueError as error:

            print("điểm số phải là số nguyên. Vui lòng nhập lại.")
            logging.error(f"nhập điểm không hợp lệ. Lỗi:{error}")

def update_score(list):

    print("--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")
    match_id = input("Nhập mã trận đấu cần cập nhật: ").strip()
    for match in list:

        if match["match_id"] == match_id:

            print(f"Trận đấu: {match['team_a']} vs {match['team_b']} : ({match['status']})")

            score_a = input_score("Đội A")
            score_b = input_score("Đội B")

            match["score_a"] = score_a
            match["score_b"] = score_b

            if score_a == 0 and score_b == 0:

                confirm = input("tỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").lower()

                if confirm == "y":
                    match["status"] = "Completed"
                else:
                    match["status"] = "Pending"

            else:
                match["status"] = "Completed"
            print(f"thành công: Đã cập nhật tỷ số trận đấu {match_id}.")

            logging.info(f"điểm số trận đấu {match_id} đã được cập nhật thành công")
            return

    print(f"Không tìm thấy trận đấu mang mã {match_id}.")

    logging.warning(f"người dùng đã cố gắng cập nhật một kết quả khớp không tồn tại {match_id}")


def determine_winner(match):
    if match["status"] == "Pending":
        return "Not Started"
    if match["score_a"] > match["score_b"]:
        return match["team_a"]
    if match["score_b"] > match["score_a"]:
        return match["team_b"]
    return "Draw"


def generate_report(list):

    print("--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")

    completed_count = 0

    for match in list:
        try:
            if match["status"] == "Completed":
                winner = determine_winner(match)
                print(
                    f"{match['match_id']}: "
                    f"{match['team_a']} {match['score_a']}-{match['score_b']} "
                    f"{match['team_b']} | Kết quả: {winner}")
                completed_count += 1

        except KeyError as error:
            logging.error(f"Thiếu khóa trong dữ liệu báo cáo: {error}")

    if completed_count == 0:
        print("Chưa có trận đấu nào hoàn thành.")

    print(f"Tổng số trận đã hoàn thành: {completed_count}")

    logging.info("Báo cáo giải đấu do người dùng tạo")


def main():
    while True:
        choice = int(input("""===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====
    1. Hiển thị lịch thi đấu & Kết quả
    2. Thêm trận đấu mới
    3. Cập nhật tỷ số trận đấu
    4. Báo cáo thống kê
    5. Thoát chương trình
    ================================================== 
    Chọn chức năng (1-5): """))
        print()
        match choice:
            case 1:
                render_matches(matches)
            case 2:
                add_match(matches)
            case 3:
                update_score(matches)   
            case 4:
                generate_report(matches)
            case 5:
                print("thoát chương trình !!!")
                break
            case _:
                print("lỗi cú pháp ! vui lòng nhập từ 1 đến 5 .....")
main()
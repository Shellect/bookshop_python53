import styles from './Profile.module.scss';

export const Profile = function () {
    let user = {
        username: "Mary Smith",
        birthdate: "20/03/2000"
    }

    return (
        <div className="row g-2">
            <div className="col-4 box-shadow p-3">
                <div className="card">
                    <img
                        src="/img/av_256.png"
                        alt="profile image"
                        className={styles['profile-img'] + " card-img-top"}
                    />
                    <div className="card-body d-grid">
                        <button type="button" className="btn btn-primary">EDIT</button>
                    </div>
                </div>
            </div>
            <div className="col-8 box-shadow p-3">
                <h5 className="text-center">{user.username}</h5>
            </div>
        </div>
    );
}
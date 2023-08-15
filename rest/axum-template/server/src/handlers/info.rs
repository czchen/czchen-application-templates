use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};
use utoipa;
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, ToSchema)]
pub struct Info {
    #[schema(example = "0.0.0")]
    version: String,
}

#[utoipa::path(
    get,
    path = "/info",
    tag = "info",
    responses(
        (status = 200, description = "get server information", body = Info),
    )
)]
pub async fn get_info() -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    Ok(Json(Info {
        version: "0.0.0".to_string(),
    }))
}

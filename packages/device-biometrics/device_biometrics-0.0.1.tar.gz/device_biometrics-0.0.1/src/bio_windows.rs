#![allow(bad_style)]
use std::sync::mpsc;
use std::time::Duration;
use windows::Security::Credentials::KeyCredentialCreationOption;
use windows::Security::Credentials::{KeyCredentialManager, KeyCredentialStatus};
use windows::Security::Cryptography::CryptographicBuffer;  // Corrected path for CryptographicBuffer
use windows::core::{HSTRING, PWSTR};  // Corrected PWSTR location to windows::core
use windows::Win32::UI::WindowsAndMessaging::{FindWindowW, SetForegroundWindow};  // UI functions
use std::ptr;

// setup returns a string and 0 if successful, or an empty string and an error code if not
pub(crate) fn setup(key_name: &str) -> Result<String, i32> {
    let key_name_hstring = HSTRING::from(key_name); // Convert &str to HSTRING

    let result = KeyCredentialManager::RequestCreateAsync(
        &key_name_hstring,
        KeyCredentialCreationOption::FailIfExists,
    )
    .map_err(|e| e.code().0)? // Map windows::core::Error to i32
    .get()
    .map_err(|e| e.code().0)?; // Map windows::core::Error to i32

    // check if we have a success or failure
    match result.Status().map_err(|e| e.code().0)? {
        KeyCredentialStatus::Success => {
            let public_key = result
                .Credential()
                .map_err(|e| e.code().0)? // Map windows::core::Error to i32
                .RetrievePublicKeyWithDefaultBlobType()
                .map_err(|e| e.code().0)?; // Map windows::core::Error to i32

            // return a base64 encoded string of the public key and 0 for success
            Ok(CryptographicBuffer::EncodeToBase64String(&public_key)
                .map_err(|e| e.code().0)? // Map windows::core::Error to i32
                .to_string())
        }
        // return an empty string and the error code
        _ => Err(result.Status().map_err(|e| e.code().0)?.0),
    }
}

// authenticate returns signed data or an error code if not successful
pub(crate) fn authenticate(key_name: &str, data_to_sign: &[u8]) -> Result<Vec<u8>, i32> {
    let key_name_hstring = HSTRING::from(key_name); // Convert &str to HSTRING
    let result = KeyCredentialManager::OpenAsync(&key_name_hstring)
        .map_err(|e| e.code().0)? // Map windows::core::Error to i32
        .get()
        .map_err(|e| e.code().0)?; // Map windows::core::Error to i32

    // if result is not successful return early
    if result.Status().map_err(|e| e.code().0)? != KeyCredentialStatus::Success {
        return Err(result.Status().map_err(|e| e.code().0)?.0);
    }
    let credential = result.Credential().map_err(|e| e.code().0)?; // Map windows::core::Error to i32
    let data = CryptographicBuffer::CreateFromByteArray(data_to_sign).map_err(|e| e.code().0)?; // Map windows::core::Error to i32

    let result = credential
        .RequestSignAsync(&data)
        .map_err(|e| e.code().0)? // Map windows::core::Error to i32
        .get()
        .map_err(|e| e.code().0)?; // Map windows::core::Error to i32

    if result.Status().map_err(|e| e.code().0)? != KeyCredentialStatus::Success {
        return Err(result.Status().map_err(|e| e.code().0)?.0);
    }

    let buffer = result.Result().map_err(|e| e.code().0)?; // Map windows::core::Error to i32

    let mut out = windows::core::Array::<u8>::with_len(buffer.Length().unwrap() as usize);
    CryptographicBuffer::CopyToByteArray(&buffer, &mut out).map_err(|e| e.code().0)?; // Map windows::core::Error to i32

    Ok(out.to_vec())

}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_setup() {
        let result = setup("test_key");
        assert!(result.is_ok());
    }

    #[test]
    fn test_authenticate() {
        let result = authenticate("test_key", b"test_data");
        assert!(result.is_ok());
    }
}
